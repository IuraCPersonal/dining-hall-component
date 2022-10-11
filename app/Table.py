import queue, random, time

from app.modules import *
from threading import Thread
from app.helpers.SafePrint import SafePrint

# Extend the Thread class to create Threads for the Tables.
class Table(Thread):
    def __init__(self, table_id, *args, **kwargs):
        super(Table, self).__init__(name=f'Table-{table_id}', *args, **kwargs)
        self.table_id = table_id
        self.__private_list = queue.Queue()

    def serve_order(self, content):
        self.__private_list.put(content)
    
    def __get_max_wait_time(self, items):
        wait_time = [FOOD[food_id]['preparation-time'] for food_id in items]
        return max(wait_time) * 1.3

    def __get_priority(self, items):
        # METHOD 1:
        priority = -len(items)
        return priority

    def __review_order(self, order):
        stars = 0
        time_stamp = order['cooking_time'] / order['max_wait']

        if time_stamp <= 1.4:
            stars = 1
        if time_stamp <= 1.3:
            stars = 2
        if time_stamp <= 1.2:
            stars = 3
        if time_stamp <= 1.1:
            stars = 4
        if time_stamp <= 1.0:
            stars = 5
        
        return stars

    def generate_order(self, waiter_id):
        order_id = order_indexer.get_index()
        items = [random.randint(1, 12) for _ in range(random.randint(1, 10))]

        order = {
            'order_id': order_id,
            'table_id': self.table_id,
            'waiter_id': waiter_id,
            'items': items,
            'priority': self.__get_priority(items),
            'max_wait': self.__get_max_wait_time(items),
            'pick_up_time': time.time()
        }

        # SafePrint.order_made(self.table_id, order_id)

        return order

    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            # Table FREE. Ordering
            time.sleep(random.randint(3, 5) * TIME_UNIT)

            # Table READY to order.
            order_queue.put(self.table_id)

            # Table SERVED. Eating
            # NOTE! the call to get() will block until an item is available to retrieve from the queue.
            order_ready = self.__private_list.get()
            order_stars = self.__review_order(order_ready)

            SafePrint.serve_order(order_ready["waiter_id"], order_ready["order_id"], order_ready["table_id"], order_stars)

            reputation_system.append(order_stars)
            SafePrint.reputation(reputation_system)