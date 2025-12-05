import os
import time
import requests
import sys
from dotenv import load_dotenv

# 1. Load keys from .env file
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# Headers
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_trello_list_id():
    """Auto-detect 'To Do' list ID from Trello Board"""
    url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
    params = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Trello Error: {response.text}")
        sys.exit(1)

    lists = response.json()
    for lst in lists:
        if lst['name'] == "To Do":
            return lst['id']
    # If 'To Do' not found, return the first list
    return lists[0]['id'] if lists else None

def get_new_leads():
    """Fetch leads from Notion that have an empty 'Trello ID'"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    payload = {"filter": {"property": "Trello ID", "rich_text": {"is_empty": True}}}
    
    response = requests.post(url, json=payload, headers=NOTION_HEADERS)
    if response.status_code != 200:
        print(f"Notion Error: {response.text}")
        return []
    return response.json().get("results", [])

def create_trello_card(list_id, name, notion_page_id):
    """Create a new card in Trello"""
    url = "https://api.trello.com/1/cards"
    query = {
        'key': TRELLO_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': name,
        'desc': f"Synced from Notion.\nNotion ID: {notion_page_id}" 
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def update_notion_lead(page_id, trello_card_id):
    """Update Notion with the Trello Card ID to prevent duplicates"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Trello ID": {"rich_text": [{"text": {"content": trello_card_id}}]}
        }
    }
    requests.patch(url, json=payload, headers=NOTION_HEADERS)

# MAIN EXECUTION LOOP

if __name__ == "__main__":
    print("Starting Sync Bot...")
    
    # Auto-find List ID
    list_id = get_trello_list_id()
    print(f"Connected to Trello! (Target List ID found)")
    print("Waiting for new leads in Notion...")

    while True:
        try:
            leads = get_new_leads()
            for lead in leads:
                props = lead["properties"]
                
                # Extract Name safely
                name = "Unnamed Lead"
                if "Name" in props and props["Name"]["title"]:
                    name = props["Name"]["title"][0]["text"]["content"]
                
                notion_id = lead["id"]
                print(f"\nNew Lead Found: {name}")
                
                # Push to Trello
                card_id = create_trello_card(list_id, name, notion_id)
                
                if card_id:
                    # Update Notion for Idempotency
                    update_notion_lead(notion_id, card_id)
                    print(f"Synced to Trello Successfully! (Card ID: {card_id})")
            
            # Poll every 5 seconds
            time.sleep(5)
            
        except Exception as e:
            print(f"Error in loop: {e}")
            time.sleep(5)