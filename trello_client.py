import os
import requests
from dotenv import load_dotenv

load_dotenv()

QUERY_PARAMS = {
    'key': os.getenv('TRELLO_KEY'),
    'token': os.getenv('TRELLO_TOKEN')
}

def create_trello_card(name, description):
    url = "https://api.trello.com/1/cards"
    # NOTE: You need to manually find your List ID (e.g. "To Do" list) first!
    # A quick way is to visit https://api.trello.com/1/boards/{BOARD_ID}/lists?key=...&token=...
    # For now, put your known List ID in the .env file
    query = {
        **QUERY_PARAMS,
        'idList': os.getenv('TRELLO_LIST_ID'),
        'name': name,
        'desc': description
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        return response.json().get('id')
    return None