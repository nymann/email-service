from abc import ABC
from abc import abstractmethod
from email.message import EmailMessage
from smtplib import SMTP
from smtplib import SMTP_SSL

from email_service.core.config import Config


class EmailServer(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config

    @abstractmethod
    def send_email(self, message: EmailMessage) -> None:
        raise NotImplementedError()


class DummyThiccEmailServer(EmailServer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.messages: list[EmailMessage] = []

    def send_email(self, message: EmailMessage) -> None:
        self.messages.append(message)


class SSLEmailServer(EmailServer):
    def __init__(self, config: Config) -> None:
        super().__init__(config=config)
        self.server = SMTP_SSL(host=config.smtp_server, port=config.smtp_port, timeout=2)
        self._setup_connection()

    def send_email(self, message: EmailMessage) -> None:
        self.server.send_message(msg=message)

    def _setup_connection(self) -> None:
        self.server.login(user=self.config.username, password=self.config.password)


class StartTLSEmailServer(EmailServer):
    def __init__(self, config: Config) -> None:
        super().__init__(config=config)
        self.server = SMTP(host=config.smtp_server, port=config.smtp_port, timeout=2)

    def send_email(self, message: EmailMessage) -> None:
        self.server.send_message(msg=message)

    def _setup_connection(self) -> None:
        self.server.starttls()
        self.server.ehlo()
        self.server.login(user=self.config.username, password=self.config.password)
