import json

from app import app
from flask import request
from app.modules import threads


# Create the 'distribution' endpoint.
@app.route('/distribution', methods=['POST'])
def distribution():
    content = request.get_json()

    # Serve prepared order recieved from KITCHEN.
    threads[f'Waiter-{content["waiter_id"]}'].serve_order(content)

    return json.dumps({'success': True}), 200