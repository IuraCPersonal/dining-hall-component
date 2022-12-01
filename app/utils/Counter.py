import threading


# Thread-Safe Counter.
class Counter:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            # logging.debug('Acquired a lock')
            self.value = self.value + 1
        finally:
            # logging.debug('Released a lock')
            self.lock.release()

    def get_index(self):
        self.increment()
        with self.lock:
            return self.value
