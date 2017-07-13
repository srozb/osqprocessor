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

    def match(self, message):
        for msg in message['message']['data']:
            if 'name' in msg:
                return True
        return False

    def run(self, message):
        "debug worker will only log the message content"
        result = []
        for msg in message['message']['data']:
            if 'name' in msg:
                result.append(msg)
        self.l.debug("data received: {}".format(self._colorify(result)))
        return message
