import os

class Config:
    TASKS_FILE = "pending_tasks.json"
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

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