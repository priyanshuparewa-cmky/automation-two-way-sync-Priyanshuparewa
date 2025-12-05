# Automation Two-Way Sync

## Overview
This project is an automation integration that connects **Notion (Lead Tracker)** with **Trello (Work Tracker)**. It ensures that when a new lead is created in Notion, a corresponding task card is automatically created in Trello. It utilizes Python and REST APIs to maintain data consistency and prevent duplicates.

## Tools Integrated
* **Lead Tracker:** Notion (Database)
* **Work Tracker:** Trello (Kanban Board)
* **Language:** Python 3
* **Libraries:** `requests`, `python-dotenv`

## Architecture & Flow

`[Notion API]  --->  [Python Script (Polling)]  --->  [Trello API]`

1.  **Poll Notion:** The script checks Notion every 5-10 seconds for leads where the `Trello ID` column is empty.
2.  **Process Data:** It extracts the Lead Name and the Notion Page ID.
3.  **Push to Trello:** It sends a POST request to Trello’s REST API to create a new card in the "To Do" list.
4.  **Update Notion (Idempotency):** Once Trello returns the new Card ID, the script updates the Notion row to save this ID. This ensures the same lead is never synced twice.

## Setup Instructions

### 1. Prerequisites
* Python 3 installed.
* A Notion Integration Token and Database ID.
* A Trello API Key, Token, and Board ID.

### 2. Installation
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration
Create a `.env` file in the root directory (do not upload this to GitHub) and add your API keys:
```ini
NOTION_TOKEN=your_notion_secret_key
NOTION_DB_ID=your_database_id
TRELLO_KEY=your_trello_key
TRELLO_TOKEN=your_trello_token
TRELLO_BOARD_ID=your_board_id
