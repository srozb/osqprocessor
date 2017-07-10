from processor.workers.abstract_worker import AbstractWorker

class Worker(AbstractWorker):
    name = "Debug Worker"
    def __init__(self):
        self._setup_logger(__name__)
    def execute(self, message):
        "debug worker will only log the message content"
        self.l.debug("processing message: {}".format(message))
        return message
