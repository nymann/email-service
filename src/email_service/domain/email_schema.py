import json

from pydantic import BaseModel


class EmailRequest(BaseModel):
    from_address: str
    to_address: str
    subject: str
    text: str | None
    html: str | None

    @classmethod
    def from_encoded_json(cls, encoded_json: str) -> "EmailRequest":
        return cls(**json.loads(encoded_json))
