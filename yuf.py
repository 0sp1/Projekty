import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from file, or return empty list if none exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save all tasks to file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def show_tasks(tasks):
    """Display all current tasks."""
    if not tasks:
        print("\nNo tasks yet!\n")
        return
    print("\nYour Tasks:")
    for i, t in enumerate(tasks, 1):
        status = "✅" if t["done"] else "❌"
        print(f"{i}. {t['title']} [{status}]")
    print()

def add_task(tasks):
    """Add a new task."""
    title = input("Enter new task: ").strip()
    if title:
        tasks.append({"title": title, "done": False})
        print(f"Added task: {title}")
    else:
        print("Task cannot be empty!")

def complete_task(tasks):
    """Mark a task as completed."""
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to complete: ")) - 1
        tasks[idx]["done"] = True
        print(f"Marked '{tasks[idx]['title']}' as done!")
    except (ValueError, IndexError):
        print("Invalid task number!")

def remove_task(tasks):
    """Delete a task from the list."""
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        removed = tasks.pop(idx)
        print(f"Removed task: {removed['title']}")
    except (ValueError, IndexError):
        print("Invalid task number!")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- TO-DO LIST ---")
        print("1. Show tasks\n2. Add task\n3. Complete task\n4. Remove task\n5. Exit")
        choice = input("Choose option: ").strip()

        if choice == "1": show_tasks(tasks)
        elif choice == "2": add_task(tasks)
        elif choice == "3": complete_task(tasks)
        elif choice == "4": remove_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
