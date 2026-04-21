from dotenv import load_dotenv
from app.task_app import TaskApp

load_dotenv()

if __name__ == "__main__":
    app = TaskApp()
    app.show_menu()