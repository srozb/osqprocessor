import json
import config
from pygments import highlight, lexers, formatters
from processor.workers.abstract_worker import AbstractWorker


class Worker(AbstractWorker):
    name = "Fancy Data Logger"

    def __init__(self):
        self._setup_logger(__name__)

    def _colorify(self, message):
        if config.DAEMON:
            return message
        buf = json.dumps(message, indent=4)
        return highlight(buf, lexers.JsonLexer(), formatters.TerminalFormatter())

    def _isEventQueryResult(self, message):
        if 'data' in message['message']:
            for msg in message['message']['data']:
                if 'name' in msg:
                    return True

    def _isDistributedQueryResult(self, message):
        return 'queries' in message['message']

    def match(self, message):
        "return True if message is a (event/distributed) query result"
        return self._isEventQueryResult(message) or self._isDistributedQueryResult(message)

    def run(self, message):
        "debug worker will only log the message content"
        if self._isEventQueryResult(message):
            result = []
            for msg in message['message']['data']:
                if 'name' in msg:
                    result.append(msg)
            self.l.debug("event query result: \n{}".format(
                self._colorify(result)))
        if self._isDistributedQueryResult(message):
            self.l.debug("distrib query result: \n{}".format(
                self._colorify(message['message']['queries'])))
        return message
