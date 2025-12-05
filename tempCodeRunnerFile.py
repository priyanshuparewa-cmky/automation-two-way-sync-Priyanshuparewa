import time
import notion_client
import trello_client

def sync_cycle():
    print("Checking for new leads in Notion...")
    
    # 1. Get leads from Notion that haven't been synced
    leads = notion_client.get_new_leads()
    
    for lead in leads:
        # Extract meaningful data from Notion's complex JSON
        props = lead["properties"]
        name_list = props["Name"]["title"]
        
        if not name_list:
            continue # Skip empty rows
            
        name = name_list[0]["text"]["content"]
        page_id = lead["id"]
        
        print(f"Syncing lead: {name}")
        
        # 2. Create Card in Trello
        card_id = trello_client.create_trello_card(name, f"Synced from Notion. ID: {page_id}")
        
        if card_id:
            # 3. Update Notion with the Trello ID so we don't sync it again (Idempotency!)
            notion_client.update_notion_trello_id(page_id, card_id)
            print(f"Successfully synced {name}!")
        else:
            print("Failed to create Trello card.")

if __name__ == "__main__":
    while True:
        sync_cycle()
        print("Sleeping for 10 seconds...")
        time.sleep(10)