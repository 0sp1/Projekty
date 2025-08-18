import os
import time

tasks = []

def show_menu():
    print("\n📋 To-Do List Manager")
    print("1. View tasks")
    print("2. Add task")
    print("3. Remove task")
    print("4. Mark task as done")
    print("5. Exit")

def view_tasks():
    if not tasks:
        print("No tasks yet! 🎉")
        return
    print("\nYour Tasks:")
    for i, (task, done) in enumerate(tasks, 1):
        status = "✅" if done else "❌"
        print(f"{i}. {task} [{status}]")

def add_task():
    task = input("Enter new task: ").strip()
    if task:
        tasks.append((task, False))
        print("Task added!")
    else:
        print("⚠️ Task cannot be empty.")

def remove_task():
    view_tasks()
    try:
        num = int(input("Enter task number to remove: "))
        tasks.pop(num - 1)
        print("Task removed!")
    except (ValueError, IndexError):
        print("⚠️ Invalid choice.")

def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        task, _ = tasks[num - 1]
        tasks[num - 1] = (task, True)
        print("Task marked as done! ✅")
    except (ValueError, IndexError):
        print("⚠️ Invalid choice.")

def main():
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
            print("👋 Goodbye! Stay productive.")
            break
        else:
            print("⚠️ Invalid option, try again.")
        time.sleep(1)

if __name__ == "__main__":
    main()
