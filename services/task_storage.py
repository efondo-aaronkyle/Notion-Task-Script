import os
import json
from typing import List
from models.task import Task

class TaskStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    return []
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2, ensure_ascii=False)