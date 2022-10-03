from email_service.core.config import Config
from email_service.domain.consumer import EmailConsumer
from email_service.domain.email_server import SSLEmailServer
from email_service.domain.email_service import EmailService


def main() -> None:
    config = Config()
    email_server = SSLEmailServer(config=config)
    email_service = EmailService(email_server=email_server)
    consumer = EmailConsumer(config=config)
    for message in consumer.consume():
        email_service.send(request=message)


if __name__ == "__main__":
    main()
