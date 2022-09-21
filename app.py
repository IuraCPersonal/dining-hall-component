# Import required libraries.
import time
import json
import queue
import random
import requests
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

# Map the table_id with it's status (FREE, READY, WAITING)
table_status = dict([(table['id'], table['status']) for table in TABLES])


# Create the 'distribution' endpoint.
@app.route('/distribution', methods=['POST'])
def distribution():
    content = request.get_json()
    table_status[content['table_id']] = FREE

    # DEBUG
    Format.log(
        f'ORDER ({content["order_id"]}) served to TABLE ({content["table_id"]})')

    # Format.log(f'TABLE [{content["table_id"]}] is FREE')

    return json.dumps({'success': True}), 200


# Extend the Thread class to create Threads for the Tables.
class Table(Thread):
    def __init__(self, table_id, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.table_id = table_id

    def generate_order(self):
        order_id = order_indexer.get_index()
        table_status[self.table_id] = WAITING
        items = [random.randint(0, 9) for _ in range(random.randint(1, 10))]

        r = requests.post(
            url=f'http://kitchen:{KITCHEN_PORT}/order',
            json={
                'order_id': order_id,
                'table_id': self.table_id,
                'items': items,
                'priority': None,
                'max_wait': None,
                'pick_up_time': time.time()
            }
        )

        Format.log(
            f'TABLE ({self.table_id}) has made ORDER ({order_id})')

    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            # Check if TABLE is busy.
            if table_status[self.table_id] == WAITING:
                time.sleep(0.50 * TIME_UNIT)
                continue

            time.sleep(random.randint(1, 16) * TIME_UNIT)

            # TODO: Implement the logic to order when READY but not when FREE.
            if table_status[self.table_id] == FREE:
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

    for index, thread in enumerate(threads):
        thread.start()
