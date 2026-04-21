from typing import List, Optional
import requests
from models.task import Task

class NotionService:
    def __init__(self, api_key: Optional[str], database_id: Optional[str]):
        self.api_key = api_key
        self.database_id = database_id
        self.url = "https://api.notion.com/v1/pages"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.database_id)

    def push_tasks(self, tasks: List[Task]) -> tuple[int, List[Task]]:
        if not self.is_configured():
            raise ValueError("Missing NOTION_API_KEY or NOTION_DATABASE_ID in .env")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        success_count = 0
        failed_tasks: List[Task] = []

        for task in tasks:
            payload = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Note": {
                        "title": [
                            {
                                "text": {
                                    "content": task.note
                                }
                            }
                        ]
                    },
                    "Subject": {
                        "select": {
                            "name": task.subject
                        }
                    },
                    "Due Date": {
                        "date": {
                            "start": task.due_date
                        }
                    },
                    "Status": {
                        "status": {
                            "name": task.status
                        }
                    },
                    "Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": task.description or ""
                                }
                            }
                        ]
                    }
                }
            }

            response = None
            try:
                response = requests.post(
                    self.url,
                    headers=headers,
                    json=payload,
                    timeout=15
                )
                response.raise_for_status()
                print(f"Task pushed: {task.note}")
                success_count += 1

            except requests.exceptions.RequestException as error:
                print(f"\nError pushing task '{task.note}': {error}")
                if response is not None:
                    print(f"Response Status Code: {response.status_code}")
                    print(f"Response Content: {response.text}")
                failed_tasks.append(task)

        return success_count, failed_tasks