# Notion Task Script

A CLI tool for managing tasks locally and syncing them to a Notion database.

## Purpose

Lets you create, view, edit, and delete tasks offline (stored in a local JSON file), then push them to Notion when you're online.

## Features

- Add tasks with subject, note, due date, status, and description
- View, edit, and delete local tasks
- Push pending tasks to a Notion database via the Notion API
- Tasks stay saved locally if you're offline or if a push fails

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:
   ```
   NOTION_API_KEY=your_notion_integration_token
   NOTION_DATABASE_ID=your_notion_database_id
   ```

3. Run the app:
   ```bash
   python main.py
   ```
   Or on Windows, double-click `run.bat`.

## Notion Database Schema

Your Notion database must have these properties:

| Property    | Type        |
|-------------|-------------|
| Note        | Title       |
| Subject     | Select      |
| Due Date    | Date        |
| Status      | Status      |
| Description | Rich Text   |

## Project Structure

```
├── app/
│   └── task_app.py       # CLI menu and task operations
├── models/
│   └── task.py           # Task data model
├── services/
│   ├── notion_service.py # Notion API integration
│   └── task_storage.py   # Local JSON read/write
├── config.py             # Subject/status options and env config
├── main.py               # Entry point
└── pending_tasks.json    # Local task storage (auto-generated)
```
