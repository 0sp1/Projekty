import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.\n")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else "✗"
        print(f"{i}. [{status}] {task['title']}")
    print()

def add_task(tasks):
    title = input("Enter task name: ").strip()
    if not title:
        print("Task name cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Task added successfully!")

def complete_task(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to complete: ")) - 1
        tasks[idx]["done"] = True
        save_tasks(tasks)
        print("Task marked as complete!")
    except (ValueError, IndexError):
        print("Invalid task number.")

def delete_task(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f"Deleted task: {removed['title']}")
    except (ValueError, IndexError):
        print("Invalid task number.")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- To-Do List Manager ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
