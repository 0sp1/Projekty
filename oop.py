import os
import time

tasks = []

FILE_NAME = "tasks.txt"

def load_tasks():
    """Load tasks from file if it exists."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                task, done = line.strip().split("|")
                tasks.append((task, done == "True"))

def save_tasks():
    """Save tasks to file."""
    with open(FILE_NAME, "w") as f:
        for task, done in tasks:
            f.write(f"{task}|{done}\n")

def show_menu():
    print("\nTo-Do List Manager")
    print("1. View tasks")
    print("2. Add task")
    print("3. Remove task")
    print("4. Mark task as done")
    print("5. Edit task")  # 👈 New option
    print("6. Exit")

def view_tasks():
    if not tasks:
        print("No tasks yet!")
        return
    print("\nYour Tasks:")
    for i, (task, done) in enumerate(tasks, 1):
        status = "Done" if done else "Not Done"
        print(f"{i}. {task} [{status}]")

def add_task():
    task = input("Enter new task: ").strip()
    if task:
        tasks.append((task, False))
        save_tasks()
        print("Task added!")
    else:
        print("Task cannot be empty.")

def remove_task():
    view_tasks()
    try:
        num = int(input("Enter task number to remove: "))
        tasks.pop(num - 1)
        save_tasks()
        print("Task removed!")
    except (ValueError, IndexError):
        print("Invalid choice.")

def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        task, _ = tasks[num - 1]
        tasks[num - 1] = (task, True)
        save_tasks()
        print("Task marked as done!")
    except (ValueError, IndexError):
        print("Invalid choice.")

def edit_task():
    """Edit the description of an existing task."""
    view_tasks()
    try:
        num = int(input("Enter task number to edit: "))
        task, done = tasks[num - 1]
        new_task = input(f"Enter new description for '{task}': ").strip()
        if new_task:
            tasks[num - 1] = (new_task, done)
            save_tasks()
            print("Task updated!")
        else:
            print("Task cannot be empty.")
    except (ValueError, IndexError):
        print("Invalid choice.")

def main():
    load_tasks()
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            remove_task()
        elif choice == "4":
            mark_done()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            print("Goodbye! Stay productive.")
            break
        else:
            print("Invalid option, try again.")
        time.sleep(1)

if __name__ == "__main__":
    main()
