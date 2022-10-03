from kafka import KafkaProducer

from email_service.domain.email_schema import EmailRequest


class EmailPublisher:
    def __init__(self, host: str, port: int, topic: str = "email", key: str | None = None) -> None:
        self.host = host
        self.port = port
        self.topic = topic
        if key is None:
            self.key = None
        else:
            self.key = key.encode("utf-8")
        self.producer = self._setup_connection()

    def publish(self, email_request: EmailRequest) -> None:
        encoded_email = email_request.json().encode("utf-8")
        self.producer.send(topic=self.topic, key=self.key, value=encoded_email)
        self.producer.flush()

    def _setup_connection(self) -> KafkaProducer:
        return KafkaProducer(bootstrap_servers=f"{self.host}:{self.port}")
