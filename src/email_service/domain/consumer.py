from typing import Iterable

from kafka import KafkaConsumer

from email_service.core.config import Config
from email_service.domain.email_schema import EmailRequest


class EmailConsumer:
    def __init__(self, config: Config, topic: str = "email") -> None:
        self.bootstrap_server = f"{config.kafka_host}:{config.kafka_port}"
        self.topic = topic
        self.client_id = f"email-service-{config.version}"
        self.consumer = self._setup_connection()

    def consume(self) -> Iterable[EmailRequest]:
        for message in self.consumer:
            yield EmailRequest.from_encoded_json(message.value)

    def _setup_connection(self) -> KafkaConsumer:
        return KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_server,
            client_id=self.client_id,
            enable_auto_commit=True,
            auto_offset_reset="latest",
        )
