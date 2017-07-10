import redis
import config
from logger.logger import Logger


class DBConn(object):
    def __init__(self):
        self.l = Logger(__name__)
        self.db = self._setup_connection()

    def _setup_connection(self):
        self.l.debug("Using redis as message backend: {}:{} db:{}".format(
            config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB))
        return redis.StrictRedis(host=config.REDIS_HOST,
                                 port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

    def get_message(self):
        "pop the message off or block"
        message = self.db.blpop('osq_preprocessed')
        return message

    def store_message(self, message):
        self.db.lpush('osq_processed', message)
