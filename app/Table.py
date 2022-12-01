import queue, time, random

from threading import Thread

from app.modules import *
from app.utils.Print import Print


# Extend the Thread class to create Threads for the Tables.
class Table(Thread):
    def __init__(self, table_id, *args, **kwargs):
        super(Table, self).__init__(name=f'Table-{table_id}', *args, **kwargs)
        self.table_id = table_id
        self.__private_list = queue.Queue()
    

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


    def generate_order(self, waiter_id):
        order_id = order_indexer.get_index()
        menu_items = restaurants.get(str(RESTAURANT_ID)).get('menu_items')
        items = [random.randint(1, menu_items) for _ in range(random.randint(1, 10))]

        order = {
            'order_id': order_id,
            'table_id': self.table_id,
            'waiter_id': waiter_id,
            'items': items,
            'priority': None,
            'max_wait': None,
            'pick_up_time': time.time()
        }

        return order


    def serve_order(self, content):
        self.__private_list.put(content)


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