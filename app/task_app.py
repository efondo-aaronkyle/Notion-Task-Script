import os
from datetime import datetime
from typing import List, Optional
import requests
from config import Config
from models.task import Task
from services.task_storage import TaskStorage
from services.notion_service import NotionService

class TaskApp:
    BOX_WIDTH = 70

    def __init__(self):
        self.storage = TaskStorage(Config.TASKS_FILE)
        self.notion_service = NotionService(
            Config.NOTION_API_KEY,
            Config.NOTION_DATABASE_ID
        )

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self) -> None:
        input("\nPress Enter to continue...")

    def print_box_header(self, title: str) -> None:
        self.clear_screen()
        print("=" * self.BOX_WIDTH)
        print(f"| {title:<{self.BOX_WIDTH - 4}} |")
        print("=" * self.BOX_WIDTH)

    def print_box_footer(self) -> None:
        print("=" * self.BOX_WIDTH)

    def print_line(self, text: str = "") -> None:
        print(f"| {text:<{self.BOX_WIDTH - 4}} |")

    def is_valid_date(self, date_text: str) -> bool:
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def print_task_summary(self, task: Task, index: int) -> None:
        text = f"[{index}] {task.note} | {task.subject} | {task.status} | {task.due_date}"
        print(text[:self.BOX_WIDTH])

    def print_task_details(self, task: Task, index: Optional[int] = None) -> None:
        self.print_box_header("Task Details")
        if index is not None:
            self.print_line(f"ID          : {index}")
        self.print_line(f"Subject     : {task.subject}")
        self.print_line(f"Note        : {task.note}")
        self.print_line(f"Due Date    : {task.due_date}")
        self.print_line(f"Status      : {task.status}")
        self.print_line(f"Description : {task.description or '-'}")
        self.print_box_footer()

    def select_from_list(self, title: str, options: List[str], allow_back: bool = False) -> Optional[str]:
        while True:
            self.print_box_header(title)

            for idx, option in enumerate(options, 1):
                self.print_line(f"{idx}. {option}")

            if allow_back:
                self.print_line("0. Back")

            self.print_box_footer()
            choice = input("Enter your choice: ").strip()

            if allow_back and choice == "0":
                return None

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                print("Invalid choice. Please select a valid option.")
                self.pause()
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.pause()

    def check_internet_connection(self) -> bool:
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def add_task(self) -> None:
        subject = self.select_from_list("Add Task - Select Subject", Config.SUBJECT_OPTIONS, allow_back=True)
        if subject is None:
            return

        self.print_box_header("Add Task")
        self.print_line("Type 0 anytime to go back.")
        self.print_box_footer()

        note = input("Enter note: ").strip()
        if note == "0":
            return

        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        if due_date == "0":
            return

        while not self.is_valid_date(due_date):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            due_date = input("Enter due date (YYYY-MM-DD) or 0 to back: ").strip()
            if due_date == "0":
                return

        status = self.select_from_list("Add Task - Select Status", Config.STATUS_OPTIONS, allow_back=True)
        if status is None:
            return

        description = input("Enter description (optional, 0 to back): ").strip()
        if description == "0":
            return

        new_task = Task(
            subject=subject,
            note=note,
            due_date=due_date,
            status=status,
            description=description,
        )

        tasks = self.storage.load_tasks()
        tasks.append(new_task)
        self.storage.save_tasks(tasks)

        print("Task added successfully!")
        self.pause()

    def view_tasks(self) -> None:
        tasks = self.storage.load_tasks()

        if not tasks:
            self.print_box_header("View Tasks")
            self.print_line("No tasks found.")
            self.print_line("0. Back")
            self.print_box_footer()
            input("Enter your choice: ")
            return

        while True:
            self.print_box_header("View Tasks")
            self.print_line("All Tasks:")
            self.print_line("-" * (self.BOX_WIDTH - 4))
            self.print_box_footer()

            for idx, task in enumerate(tasks):
                self.print_task_summary(task, idx)

            print("=" * self.BOX_WIDTH)
            print("Enter task ID to view details")
            print("0. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "0":
                return

            try:
                index = int(choice)
                if 0 <= index < len(tasks):
                    self.print_task_details(tasks[index], index)
                    self.pause()
                else:
                    print("Invalid task ID.")
                    self.pause()
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.pause()

    def edit_task(self) -> None:
        tasks = self.storage.load_tasks()

        if not tasks:
            self.print_box_header("Edit Task")
            self.print_line("No tasks available to edit.")
            self.print_line("0. Back")
            self.print_box_footer()
            input("Enter your choice: ")
            return

        while True:
            self.print_box_header("Edit Task")
            self.print_line("Select a task to edit:")
            self.print_box_footer()

            for idx, task in enumerate(tasks):
                self.print_task_summary(task, idx)

            print("=" * self.BOX_WIDTH)
            print("0. Back")

            choice = input("Enter task ID to edit: ").strip()

            if choice == "0":
                return

            try:
                index = int(choice)
                if not (0 <= index < len(tasks)):
                    print("Invalid task ID.")
                    self.pause()
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.pause()
                continue

            task = tasks[index]

            while True:
                self.print_box_header(f"Edit Task [{index}]")
                self.print_line("1. Subject")
                self.print_line("2. Note")
                self.print_line("3. Due Date")
                self.print_line("4. Status")
                self.print_line("5. Description")
                self.print_line("0. Back")
                self.print_box_footer()

                field_choice = input("Enter the number of the field to edit: ").strip()

                if field_choice == "0":
                    return
                elif field_choice == "1":
                    new_subject = self.select_from_list("Edit Subject", Config.SUBJECT_OPTIONS, allow_back=True)
                    if new_subject:
                        task.subject = new_subject
                elif field_choice == "2":
                    new_note = input("Enter new note (or 0 to back): ").strip()
                    if new_note == "0":
                        continue
                    task.note = new_note
                elif field_choice == "3":
                    new_due_date = input("Enter new due date (YYYY-MM-DD) or 0 to back: ").strip()
                    if new_due_date == "0":
                        continue
                    while not self.is_valid_date(new_due_date):
                        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                        new_due_date = input("Enter new due date (YYYY-MM-DD) or 0 to back: ").strip()
                        if new_due_date == "0":
                            break
                    if new_due_date != "0" and self.is_valid_date(new_due_date):
                        task.due_date = new_due_date
                elif field_choice == "4":
                    new_status = self.select_from_list("Edit Status", Config.STATUS_OPTIONS, allow_back=True)
                    if new_status:
                        task.status = new_status
                elif field_choice == "5":
                    new_description = input("Enter new description (or 0 to back): ").strip()
                    if new_description == "0":
                        continue
                    task.description = new_description
                else:
                    print("Invalid choice.")
                    self.pause()
                    continue

                self.storage.save_tasks(tasks)
                print("Task updated successfully!")
                self.pause()
                return

    def delete_task(self) -> None:
        tasks = self.storage.load_tasks()

        if not tasks:
            self.print_box_header("Delete Task")
            self.print_line("No tasks available to delete.")
            self.print_line("0. Back")
            self.print_box_footer()
            input("Enter your choice: ")
            return

        while True:
            self.print_box_header("Delete Task")
            self.print_line("Select a task to delete:")
            self.print_box_footer()

            for idx, task in enumerate(tasks):
                self.print_task_summary(task, idx)

            print("=" * self.BOX_WIDTH)
            print("0. Back")

            choice = input("Enter task ID to delete: ").strip()

            if choice == "0":
                return

            try:
                index = int(choice)
                if not (0 <= index < len(tasks)):
                    print("Invalid task ID.")
                    self.pause()
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.pause()
                continue

            confirm = input(f"Are you sure you want to delete task [{index}]? (y/n): ").strip().lower()
            if confirm == "y":
                deleted_task = tasks.pop(index)
                self.storage.save_tasks(tasks)
                print(f"Task deleted successfully: {deleted_task.note}")
                self.pause()
                return
            else:
                print("Delete cancelled.")
                self.pause()
                return

    def push_to_notion(self) -> None:
        self.print_box_header("Push Tasks to Notion")
        tasks = self.storage.load_tasks()

        if not tasks:
            self.print_line("No offline tasks found to push.")
            self.print_box_footer()
            self.pause()
            return

        if not self.notion_service.is_configured():
            self.print_line("Missing NOTION_API_KEY or NOTION_DATABASE_ID in .env")
            self.print_box_footer()
            self.pause()
            return

        self.print_box_footer()

        try:
            success_count, failed_tasks = self.notion_service.push_tasks(tasks)

            if success_count > 0:
                self.storage.save_tasks(failed_tasks)
                print(f"\nDone. {success_count} task(s) pushed to Notion.")
                print(f"{len(failed_tasks)} task(s) remaining offline.")
            else:
                print("\nNo tasks were pushed. All tasks remain saved offline.")
        except ValueError as error:
            print(str(error))

        self.pause()

    def show_menu(self) -> None:
        while True:
            self.print_box_header("Task Automation Menu")
            self.print_line("1. Add Task")
            self.print_line("2. View Tasks")
            self.print_line("3. Edit Task")
            self.print_line("4. Delete Task")
            self.print_line("5. Push Tasks to Notion (Online Only)")
            self.print_line("6. Exit")
            self.print_box_footer()

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.edit_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                if self.check_internet_connection():
                    self.push_to_notion()
                else:
                    print("You are offline. Tasks will stay saved locally.")
                    self.pause()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")
                self.pause()