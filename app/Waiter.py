import queue
import requests

from app.modules import *
from threading import Thread, Lock
from app.utils.Print import Print


# Extend the Thread class to create Threads for the Waiters.
class Waiter(Thread):
    def __init__(self, waiter_id, *args, **kwargs):
        super(Waiter, self).__init__(name=f'Waiter-{waiter_id}', *args, **kwargs)
        self.waiter_id = waiter_id
        self.__private_list = queue.Queue()
        self.__lock = Lock()


    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            try:
                finished_order = self.__private_list.get(timeout=(2*TIME_UNIT))
                threads[f'Table-{finished_order["table_id"]}'].serve_order(finished_order)
            except queue.Empty:
                pass
            except KeyError:
                pass

            try:
                # This line will raise queue.Empty if the queue is actually empty
                free_table_id = order_queue.get(block=False)

                order = threads[f'Table-{free_table_id}'].generate_order(self.waiter_id)
                items = order.get('items')
                
                order['priority'] = self.__get_priority(items)
                order['max_wait'] = self.__get_max_wait_time(items)

                Print.took_order(self.waiter_id, order["order_id"], order["table_id"])

                _ = requests.post(
                    url=f'http://kitchen-{RESTAURANT_ID}:{KITCHEN_PORT}/order',
                    json=order
                )
            except queue.Empty:
                pass
        
            
            # Check if there are any online orders waiting to be indexed and sent to kitchen.
            try:
                online_order = online_order_queue.get(block=False)
                items = online_order.get('items')

                online_order.update({
                    'order_id': order_indexer.get_index(),
                    'is_ready': False,
                    'priority': self.__get_priority(items),
                    'max_wait': self.__get_max_wait_time(items),
                    'waiter_id': self.waiter_id
                })

                _ = requests.post(
                    url=f'http://kitchen-{RESTAURANT_ID}:{KITCHEN_PORT}/order',
                    json=online_order
                )
            except queue.Empty:
                pass


    def __get_max_wait_time(self, items):
        wait_time = [
            restaurants.get(str(RESTAURANT_ID)).get('menu').get(str(item)).get('preparation-time') 
            for item in items
        ]

        return max(wait_time) * 1.3


    def __get_priority(self, items):
        priority = sum(
            restaurants.get(str(RESTAURANT_ID)).get('menu').get(str(item)).get('preparation-time') 
            for item in items
        )

        return priority

    def serve_order(self, content):
        with self.__lock:
            self.__private_list.put(content)