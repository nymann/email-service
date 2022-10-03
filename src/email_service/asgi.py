from email_service.api import Api
from email_service.core.config import Config
from email_service.core.service_container import ServiceContainer

config = Config()
service_container = ServiceContainer(config=config)
api = Api(config=config, service_container=service_container).api
