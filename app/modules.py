import os, json, queue
from app.utils.Counter import Counter

# Function to read the content of a JSON file.
def read_json(file):    
    current_directory = os.getcwd()
    with open(f'./{current_directory}/data/{file}', 'r') as f:
        data = json.load(f)
    
    return data


threads = dict()
restaurants = read_json('restaurants.json').get('restaurants')

order_queue = queue.Queue()
online_order_queue = queue.Queue()

order_indexer = Counter()

HOST_NAME = os.getenv('HOST_NAME')
RESTAURANT_ID = os.getenv('RESTAURANT_ID')
TIME_UNIT = int(os.getenv('TIME_UNIT'))

FOOD_ORDERING_PORT = os.getenv('FOOD_ORDERING_PORT')
KITCHEN_PORT = restaurants.get(str(RESTAURANT_ID)).get('kitchen-port')
DINING_HALL_PORT = restaurants.get(str(RESTAURANT_ID)).get('dining-port')

AMOUNT_OF_TABLES = int(os.getenv('AMOUNT_OF_TABLES'))
NUMBER_OF_WAITERS = int(os.getenv('NUMBER_OF_WAITERS'))