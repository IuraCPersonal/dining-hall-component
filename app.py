# Import required libraries.
import time
import requests
import json
import random
import logging

from modules import *
from threading import Thread
from flask import Flask, request

# Setup Flask and other dependencies.
app = Flask(__name__)
order_indexer = Counter()

# Disable Flask console messages.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Map the table_id with it's status.
table_status = dict([(table['id'], table['status']) for table in TABLES])


# Create the 'distribution' endpoint.
@app.route('/distribution', methods=['POST'])
def distribution():
    content = request.get_json()
    table_status[content['table_id']] = FREE

    # DEBUG:
    Format.log(
        f'Order {content["order_id"]} served to Table {content["table_id"]}')

    return json.dumps({'success': True}), 200

# Extend Thread class to create Threads for the Tables.
class Table(Thread):
    def __init__(self, table_id, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.table_id = table_id

    def generate_order(self):
        items = [random.randint(0, 9) for _ in range(random.randint(1, 10))]
        table_status[self.table_id] = WAITING
        order_id = order_indexer.get_index()

        r = requests.post(
            url=f'http://kitchen:{KITCHEN_PORT}/order',
            json={
                'order_id': order_id,
                'table_id': self.table_id,
                'items': items,
                'pick_up_time': time.time()
            }
        )

        Format.log(
            f'Table {self.table_id} has made order No. {order_id}')

    # Override the run() function of Thread class.
    def run(self):
        while True:
            if table_status[self.table_id] == WAITING:
                time.sleep(0.25 * TIME_UNIT)
                continue

            time.sleep(random.randint(2, 10) * TIME_UNIT)
            self.generate_order()


if __name__ == '__main__':
    threads = list()

    threads.append(
        Thread(target=lambda: app.run(
            host=HOST_NAME,
            port=DINING_HALL_PORT,
            debug=False,
            use_reloader=False
        ))
    )
    
    for index in range(1, AMOUNT_OF_TABLES + 1):
        table = Table(index)
        threads.append(table)
        table_status[table.table_id] = FREE

    for index, thread in enumerate(threads):
        thread.start()
