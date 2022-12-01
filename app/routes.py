import json, time

from app import app
from flask import request

from app.modules import threads, online_order_queue


# Create the 'distribution' endpoint.
@app.route('/distribution', methods=['POST'])
def distribution():
    content = request.get_json()

    # Serve prepared order recieved from KITCHEN.
    threads[f'Waiter-{content["waiter_id"]}'].serve_order(content)

    return json.dumps({'success': True}), 200


# Create the '/v2/order' endpoint.
@app.route('/v2/order', methods=['POST'])
def v2order():
    content = request.get_json()

    content['registered_time'] = time.time()

    online_order_queue.put(content)

    print(content)

    return json.dumps({'success': True}), 200