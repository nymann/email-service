from pydantic import BaseSettings

from email_service.version import __version__


class Config(BaseSettings):
    version: str = __version__
    username: str
    password: str
    smtp_server: str
    smtp_port: int
    kafka_host: str
    kafka_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
