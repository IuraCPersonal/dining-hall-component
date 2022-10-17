import logging

from flask import Flask
from threading import Thread

from app.modules import *
from app.Table import Table
from app.Waiter import Waiter


# Disable Flask console messages.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Setup Flask and other dependencies.
app = Flask(__name__)

from app import routes

threads['Flask'] = (
    Thread(
        name='Flask',
        target=lambda: app.run(
            host=HOST_NAME,
            port=DINING_HALL_PORT,
            debug=False,
            use_reloader=False
        )
    )
)

for index in range(1, AMOUNT_OF_TABLES + 1):
    table = Table(index)
    threads[table.name] = table

for index in range(1, NUMBER_OF_WAITERS + 1):
    waiter = Waiter(index)
    threads[waiter.name] = waiter

for index, thread in enumerate(threads.values()):
    thread.start()
