import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_new_leads():
    url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DB_ID')}/query"
    # We filter for leads that DO NOT have a Trello ID yet (meaning they are not synced)
    payload = {
        "filter": {
            "property": "Trello ID",
            "rich_text": {
                "is_empty": True
            }
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code != 200:
        print("Error fetching Notion:", response.text)
        return []
    return response.json().get("results", [])

def update_notion_trello_id(page_id, trello_card_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Trello ID": {
                "rich_text": [{"text": {"content": trello_card_id}}]
            }
        }
    }
    requests.patch(url, json=payload, headers=HEADERS)