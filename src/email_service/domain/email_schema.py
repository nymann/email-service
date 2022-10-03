from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import formatdate
import json
import mimetypes
from pathlib import Path

from pydantic import BaseModel


class EmailAddress(BaseModel):
    name: str
    email: str

    def to_address(self) -> Address:
        username, domain = self.email.split("@")
        return Address(display_name=self.name, domain=domain, username=username)


class Attachment(BaseModel):
    binary_data: bytes
    filename: str
    maintype: str
    subtype: str

    @classmethod
    def from_file(cls, attachment: Path) -> "Attachment":
        mimetype = mimetypes.types_map.get(attachment.suffix, "data/octet-stream")
        maintype, subtype = mimetype.split("/")
        with open(file=attachment, mode="rb") as fp:
            binary_data = fp.read()
        return cls(
            binary_data=binary_data,
            filename=attachment.name,
            maintype=maintype,
            subtype=subtype,
        )


class EmailRequest(BaseModel):
    from_address: EmailAddress
    to_address: EmailAddress
    subject: str
    text: str | None
    html: str | None
    bcc: list[EmailAddress] | None = None
    cc: list[EmailAddress] | None = None
    attachments: list[Attachment] = []

    @classmethod
    def from_encoded_json(cls, encoded_json: str) -> "EmailRequest":
        return cls(**json.loads(encoded_json))

    def message(self) -> EmailMessage:
        msg = EmailMessage()
        msg.set_content(self.text)
        if self.html:
            msg.add_alternative(self.html, subtype="html")
        msg["Subject"] = self.subject
        msg["From"] = self.from_address.to_address()
        msg["To"] = self.to_address.to_address()
        msg["Date"] = formatdate(localtime=True)
        if self.bcc:
            msg["Bcc"] = (bcc.to_address() for bcc in self.bcc)
        if self.cc:
            msg["Cc"] = (cc.to_address() for cc in self.cc)

        for attachment in self.attachments:
            msg.add_attachment(
                attachment.binary_data,
                maintype=attachment.maintype,
                subtype=attachment.subtype,
                filename=attachment.filename,
            )

        return msg
