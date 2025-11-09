import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

class Task:
    def __init__(self, title, completed=False, created_at=None):
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at
        }

class ToDoList:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as file:
            try:
                data = json.load(file)
                return [Task(**task) for task in data]
            except json.JSONDecodeError:
                return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([t.to_dict() for t in self.tasks], file, indent=4)

    def add_task(self, title):
        self.tasks.append(Task(title))
        self.save_tasks()
        print(f"Added task: '{title}'")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\nYour Tasks:")
        for i, task in enumerate(self.tasks, start=1):
            status = "Done" if task.completed else "Pending"
            print(f"{i}. [{status}] {task.title} (created {task.created_at})")

    def complete_task(self, index):
        try:
            task = self.tasks[index - 1]
            task.completed = True
            self.save_tasks()
            print(f"Task '{task.title}' marked as complete.")
        except IndexError:
            print("Invalid task number.")

    def delete_task(self, index):
        try:
            task = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"Deleted task '{task.title}'")
        except IndexError:
            print("Invalid task number.")

def main():
    todo = ToDoList()
    while True:
        print("\n--- TO-DO LIST ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            todo.list_tasks()
        elif choice == "2":
            title = input("Enter task title: ").strip()
            if title:
                todo.add_task(title)
        elif choice == "3":
            todo.list_tasks()
            try:
                num = int(input("Enter task number to complete: "))
                todo.complete_task(num)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            todo.list_tasks()
            try:
                num = int(input("Enter task number to delete: "))
                todo.delete_task(num)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
