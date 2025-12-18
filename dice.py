import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, description, priority, due_date):
        task = {
            "description": description,
            "completed": False,
            "priority": priority,
            "due_date": due_date
        }
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully.")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return

        today = datetime.today().date()

        for i, task in enumerate(self.tasks, 1):
            status = "Completed" if task["completed"] else "Pending"
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            overdue = "OVERDUE" if not task["completed"] and due < today else ""
            print(
                f"{i}. {task['description']} "
                f"[{status}] | Priority: {task['priority']} | Due: {task['due_date']} {overdue}"
            )

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()
            print("Task marked as completed.")
        else:
            print("Invalid task number.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            print(f"Deleted task: {removed['description']}")
        else:
            print("Invalid task number.")

    def edit_task(self, index, description, priority, due_date):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["description"] = description
            self.tasks[index]["priority"] = priority
            self.tasks[index]["due_date"] = due_date
            self.save_tasks()
            print("Task updated successfully.")
        else:
            print("Invalid task number.")

def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Edit task")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            manager.view_tasks()

        elif choice == "2":
            desc = input("Enter task description: ")
            priority = input("Priority (Low / Medium / High): ").capitalize()
            due_date = input("Due date (YYYY-MM-DD): ")
            manager.add_task(desc, priority, due_date)

        elif choice == "3":
            manager.view_tasks()
            try:
                num = int(input("Enter task number to complete: ")) - 1
                manager.complete_task(num)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            manager.view_tasks()
            try:
                num = int(input("Enter task number to delete: ")) - 1
                manager.delete_task(num)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            manager.view_tasks()
            try:
                num = int(input("Enter task number to edit: ")) - 1
                desc = input("New description: ")
                priority = input("New priority (Low / Medium / High): ").capitalize()
                due_date = input("New due date (YYYY-MM-DD): ")
                manager.edit_task(num, desc, priority, due_date)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
