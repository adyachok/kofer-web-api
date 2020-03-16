import os

from motor.motor_asyncio import AsyncIOMotorClient

from models.faust_dao import ModelTask, ModelMetadata
from repositories.mongo_repo import MongoRepository
from utils.logger import get_logger


logger = get_logger('config')


class Config:

    REQUEST_INTERVAL = None
    KAFKA_BROKER_URL = None

    def __init__(self):
        """
        Initiates microservice configuration
        :return: configuration object
        """
        self.REQUEST_INTERVAL = self._set_request_interval()
        self.KAFKA_BROKER_URL = self._set_kafka_url()
        self.MONGO_DB_CLIENT = self._set_mongo_db_client()
        self.mongo_repo = self._set_mongo_repository()
        self.topics = {
            'model-tasks-do': None,
            'model-tasksdone': None,
            'model-metadata-updates': None
        }

    def _set_request_interval(self):
        request_interval = os.getenv('ZZ_MONITOR_REQUEST_INTERVAL')
        return int(request_interval) if request_interval else 2

    def _set_kafka_url(self):
        kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
        if not kafka_broker_url:
            kafka_broker_url = 'kafka://localhost'
        return kafka_broker_url

    def _set_mongo_db_client(self):
        url = os.getenv('MONGO_URL')
        if not url:
            url = 'mongodb://web_api:secret@localhost:27017'
        db = os.getenv('WEB-API-MONGO_DB')
        if not db:
            db = 'web-api'
        return AsyncIOMotorClient(url)[db]

    def _set_mongo_repository(self):
        if not self.MONGO_DB_CLIENT:
            self.MONGO_DB_CLIENT = self._set_mongo_db_client()
        return MongoRepository(self.MONGO_DB_CLIENT)

    def init_app(self, app):
        self._init_topics(app)

    def _init_topics(self, app):
        self.topics['model-tasks-do'] = app.topic('model-tasks-do',
                                                  value_type=ModelTask)
        self.topics['model-tasks-done'] = app.topic('model-tasks-done',
                                                    value_type=ModelTask)
        self.topics['model-metadata-updates'] = app.topic(
            'model-metadata-updates', value_type=ModelMetadata)
