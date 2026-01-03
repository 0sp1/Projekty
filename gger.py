import os
import json
from datetime import datetime

class Task:
    def __init__(self, title, due_date=None, completed=False):
        self.title = title
        self.due_date = due_date
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["due_date"], data["completed"])

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, due_date=None):
        task = Task(title, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for idx, task in enumerate(self.tasks, 1):
            status = "✔" if task.completed else "✘"
            due = f" (Due: {task.due_date})" if task.due_date else ""
            print(f"{idx}. {task.title}{due} [{status}]")

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]

def menu():
    manager = TaskManager()
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task Completed")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            due_date = input("Enter due date (YYYY-MM-DD) or leave empty: ")
            due_date = due_date if due_date else None
            manager.add_task(title, due_date)
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            manager.list_tasks()
            idx = int(input("Enter task number: ")) - 1
            manager.mark_completed(idx)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
