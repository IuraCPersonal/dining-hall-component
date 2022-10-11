import json

from app import app
from flask import request
from app.modules import threads


# Create the 'distribution' endpoint.
@app.route('/distribution', methods=['POST'])
def distribution():
    content = request.get_json()
    # table_status[content['table_id']] = FREE

    # Serve prepared order recieved from KITCHEN.
    threads[f'Waiter-{content["waiter_id"]}'].serve_order(content)

    # DEBUG
    # Format.log(
    #     f'ORDER ({content["order_id"]}) served to TABLE ({content["table_id"]})')

    # Format.log(f'TABLE [{content["table_id"]}] is FREE')

    return json.dumps({'success': True}), 200