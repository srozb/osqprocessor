from logger.logger import Logger

class AbstractWorker(object):
    name = "Abstract Worker"
    def __init__(self):
        ""
    def __repr__(self):
        return self.name
    def _setup_logger(self, mod_name):
        self.l = Logger(mod_name)
    def match(self, message):
        return True
    def execute(self, message):
        return message
    def run(self, message):
        "run execute with try wrapper"
        try:
            message = self.execute(message)
        except Exception as e:
            self.l.error("EXCEPTION: {}".format(e))
        return message
