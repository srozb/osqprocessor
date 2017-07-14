#!/usr/bin/env python3

import daemon
import config
from processor.processor import Processor
from processor.workers import debug_worker, fancy_logger
from logger.logger import Logger
from dbconn.dbconn import DBConn

INSTALLED_WORKERS = [fancy_logger]


def setup_processor():
    p = Processor()
    for worker in INSTALLED_WORKERS:
        p.register(worker.Worker())
    return p

def setup_db():
    return DBConn()

def main():
    if config.DAEMON:
        print("daemonizing...")
        with daemon.DaemonContext():
            loop()
    else:
        l.debug("osqprocessor initialized, entering main loop")
        loop()

def loop():
    p = setup_processor()
    r = setup_db()
    while True:
        message = r.get_message()
        p.process(message)
        r.store_message(message)

l = Logger(__name__)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        l.info("Keyboard interrupt catched. Closing...")
