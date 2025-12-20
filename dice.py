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
        self.tasks.append({
            "description": description,
            "completed": False,
            "priority": priority,
            "due_date": due_date
        })
        self.save_tasks()
        print("Task added successfully.")

    def view_tasks(self, tasks=None):
        tasks = tasks if tasks is not None else self.tasks

        if not tasks:
            print("No tasks found.")
            return

        today = datetime.today().date()

        for i, task in enumerate(tasks, 1):
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

    def filter_tasks(self, mode):
        today = datetime.today().date()
        filtered = []

        for task in self.tasks:
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

            if mode == "completed" and task["completed"]:
                filtered.append(task)
            elif mode == "pending" and not task["completed"]:
                filtered.append(task)
            elif mode == "overdue" and not task["completed"] and due < today:
                filtered.append(task)
            elif mode in ("low", "medium", "high") and task["priority"].lower() == mode:
                filtered.append(task)

        self.view_tasks(filtered)

    def search_tasks(self, keyword):
        keyword = keyword.lower()
        results = [
            task for task in self.tasks
            if keyword in task["description"].lower()
        ]
        self.view_tasks(results)

def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Edit task")
        print("6. Filter tasks")
        print("7. Search tasks")
        print("8. Exit")

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
            print("1. Completed")
            print("2. Pending")
            print("3. Overdue")
            print("4. Low priority")
            print("5. Medium priority")
            print("6. High priority")

            option = input("Choose filter: ")

            modes = {
                "1": "completed",
                "2": "pending",
                "3": "overdue",
                "4": "low",
                "5": "medium",
                "6": "high"
            }

            if option in modes:
                manager.filter_tasks(modes[option])
            else:
                print("Invalid filter option.")

        elif choice == "7":
            keyword = input("Enter keyword to search: ")
            manager.search_tasks(keyword)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
