from dataclasses import dataclass, asdict

@dataclass
class Task:
    subject: str
    note: str
    due_date: str
    status: str
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            subject=data.get("subject", ""),
            note=data.get("note", ""),
            due_date=data.get("due_date", ""),
            status=data.get("status", "Not started"),
            description=data.get("description", ""),
        )