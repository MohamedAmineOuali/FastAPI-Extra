import logging

from mongoengine import connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongodbService:
    def __init__(
            self, db, alias, username, password, host, authentication_source, port=27017
    ):
        self.db = db
        self.alias = alias
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.authentication_source = authentication_source

    async def connect(self):
        logger.info(
            "Connecting to mongo database={0} with alias={1}, on host={2}:{3}".format(
                self.db, self.alias, self.host, self.port
            )
        )
        self.conn = connect(
            db=self.db,
            alias=self.alias,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            authentication_source=self.authentication_source,
        )
        return self.conn

    def __enter__(self):
        return self.connect()

    async def disconnect(self, ):
        logger.info(
            "Disconnecting to mongo database={0} with alias={1}, on host={2}:{3}".format(
                self.db, self.alias, self.host, self.port
            )
        )
        self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()