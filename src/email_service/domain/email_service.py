import logging
import sys

from email_service.domain.email_schema import EmailRequest
from email_service.domain.email_server import EmailServer

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class EmailService:
    def __init__(self, email_server: EmailServer) -> None:
        self.email_server = email_server

    def send(self, request: EmailRequest) -> None:
        self.email_server.send_email(message=request.message())
        logging.info(
            "'%s' from '%s' to '%s'",
            request.subject,
            request.from_address,
            request.to_address,
        )
