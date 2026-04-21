import os

class Config:
    TASKS_FILE = "pending_tasks.json"

    SUBJECT_OPTIONS = [
        "Personal",
        "App Development",
        "Capstone Project 1",
        "Ethics",
        "Information Assurance and Security",
        "Elective 2",
        "Principles of Organization and Management",
        "The Contemporary World",
    ]

    STATUS_OPTIONS = [
        "Not started",
        "In progress",
        "Done",
    ]

    @staticmethod
    def get_notion_api_key():
        return os.getenv("NOTION_API_KEY")

    @staticmethod
    def get_notion_database_id():
        return os.getenv("NOTION_DATABASE_ID")