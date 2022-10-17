import queue, random, time
from threading import Thread

from app.modules import *
from app.helpers.Print import Print


# Extend the Thread class to create Threads for the Tables.
class Table(Thread):
    def __init__(self, table_id, *args, **kwargs):
        super(Table, self).__init__(name=f'Table-{table_id}', *args, **kwargs)
        self.table_id = table_id
        self.__private_list = queue.Queue()
    
    def __get_max_wait_time(self, items):
        wait_time = [FOOD[food_id]['preparation-time'] for food_id in items]
        return max(wait_time) * 1.3

    def __get_priority(self, items):
        # METHOD 1:
        # priority = len(items)

        # METHOD 2:
        priority = sum(FOOD[item]["preparation-time"] for item in items)
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
    
    # Overide the run() method of the Thread class.
    def run(self):
        while True:
            # Table FREE. Waiting for people to come...
            time.sleep(random.randint(5, 30) * TIME_UNIT)

            # Table READY to order.
            order_queue.put(self.table_id)

            # NOTE! the call to get() will block until an item is available to retrieve from the queue.
            order_ready = self.__private_list.get()
            # Table SERVED. Eating...
            order_stars = self.__review_order(order_ready)

            Print.serve_order(order_ready["waiter_id"], order_ready["order_id"], order_ready["table_id"], order_stars)

            reputation_system.append(order_stars)
            Print.reputation(reputation_system)

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

        return order

    def serve_order(self, content):
        self.__private_list.put(content)