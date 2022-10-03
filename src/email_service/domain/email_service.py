from email.message import EmailMessage
from email.utils import formatdate

from email_service.domain.email_schema import EmailRequest
from email_service.domain.email_server import EmailServer


class EmailService:
    def __init__(self, email_server: EmailServer) -> None:
        self.email_server = email_server

    def send(self, message: EmailRequest) -> None:
        msg = EmailMessage()
        msg.set_content(message.text)
        if message.html:
            msg.add_alternative(message.html, subtype="html")
        msg["Subject"] = message.subject
        msg["From"] = message.from_address
        msg["To"] = message.to_address
        msg["Date"] = formatdate(localtime=True)
        self.email_server.send_email(message=msg)
