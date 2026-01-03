import os
import json

class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, description):
        """Add a new task."""
        self.tasks.append({"task": description, "done": False})
        self.save_tasks()
        print(f"Added: '{description}'")

    def list_tasks(self):
        """List all tasks."""
        if not self.tasks:
            print("No tasks yet!")
            return
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["done"] else "✗"
            print(f"{i}. [{status}] {task['task']}")

    def mark_done(self, index):
        """Mark a task as done."""
        try:
            self.tasks[index - 1]["done"] = True
            self.save_tasks()
            print("Task marked as done!")
        except IndexError:
            print("Invalid task number.")

    def delete_task(self, index):
        """Delete a task."""
        try:
            removed = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"Deleted: '{removed['task']}'")
        except IndexError:
            print("Invalid task number.")


def main():
    todo = TodoList()
    print("📋 Simple To-Do List")
    print("Commands: add, list, done, delete, quit")

    while True:
        cmd = input("\nEnter command: ").strip().lower()

        if cmd == "add":
            desc = input("Task description: ").strip()
            if desc:
                todo.add_task(desc)
        elif cmd == "list":
            todo.list_tasks()
        elif cmd == "done":
            num = int(input("Task number: "))
            todo.mark_done(num)
        elif cmd == "delete":
            num = int(input("Task number: "))
            todo.delete_task(num)
        elif cmd == "quit":
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
