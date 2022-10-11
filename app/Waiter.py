import queue
import requests

from app.modules import *
from threading import Thread
from app.helpers.SafePrint import SafePrint

# Extend the Thread class to create Threads for the Waiters.
class Waiter(Thread):
    def __init__(self, waiter_id, *args, **kwargs):
        super(Waiter, self).__init__(
            name=f'Waiter-{waiter_id}', *args, **kwargs)
        self.waiter_id = waiter_id
        self.__private_list = queue.Queue()

    def run(self):
        while True:
            try:
                finished_order = self.__private_list.get(timeout=(3))
                threads[f'Table-{finished_order["table_id"]}'].serve_order(
                    finished_order)
            except queue.Empty:
                pass

            try:
                # This line will raise queue.Empty if the queue is actually empty
                free_table_id = order_queue.get(block=False)
                order = threads[f'Table-{free_table_id}'].generate_order(
                    self.waiter_id)

                SafePrint.took_order(self.waiter_id, order["order_id"], order["table_id"])

                _ = requests.post(
                    url=f'http://kitchen:{KITCHEN_PORT}/order',
                    json=order
                )

            except queue.Empty:
                pass

    def serve_order(self, content):
        self.__private_list.put(content)