import dataset
from datetime import datetime
from processor.workers.abstract_worker import AbstractWorker
import config


class Worker(AbstractWorker):
    name = "Inventory Worker"

    def __init__(self):
        self._setup_logger(__name__)
        self.db = dataset.connect(config.DB_URL)

    def _isInventoryQueryResult(self, message):
        if 'data' not in message['message']:
            return False
        for msg in message['message']['data']:
            if 'name' in msg and msg['action'] == 'added' and msg['name'] == 'Inventory OS':
                self.inventory_msg = msg['columns']
                self.host_identifier = msg['hostIdentifier']
                self.client_id = message['client']['client_id']
                return True

    def _updateInventory(self):
        "update client inventory"
        self.l.debug("updating machine inventory with: uuid:{} ({platform} {version})".format(
            self.host_identifier, **self.inventory_msg))
        client_table = self.db['osquery_client']
        client_table.update(
            dict(id=self.client_id,
                 last_communication=datetime.utcnow(),
                 uuid=self.host_identifier,
                 platform=self.inventory_msg['platform'],
                 os_name=self.inventory_msg['name'],
                 os_version=self.inventory_msg['version']), ['id'])

    def match(self, message):
        return self._isInventoryQueryResult(message)

    def run(self, message):
        "Process message and update the DB."
        self._updateInventory()
        return message
