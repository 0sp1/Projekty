# To-Do List App (Konsolowa)

tasks = []

def show_menu():
    print("\n--- MENU ---")
    print("1. Pokaż zadania")
    print("2. Dodaj zadanie")
    print("3. Usuń zadanie")
    print("4. Oznacz jako ukończone")
    print("5. Wyjście")

def show_tasks():
    if not tasks:
        print("Brak zadań.")
    else:
        for idx, task in enumerate(tasks, 1):
            status = "✓" if task['done'] else "✗"
            print(f"{idx}. [{status}] {task['title']}")

def add_task():
    title = input("Wpisz treść zadania: ")
    tasks.append({'title': title, 'done': False})
    print("Dodano zadanie.")

def delete_task():
    show_tasks()
    try:
        idx = int(input("Numer zadania do usunięcia: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            print(f"Usunięto zadanie: {removed['title']}")
        else:
            print("Nieprawidłowy numer.")
    except ValueError:
        print("Wprowadź liczbę.")

def mark_done():
    show_tasks()
    try:
        idx = int(input("Numer zadania do oznaczenia jako ukończone: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]['done'] = True
            print(f"Zadanie \"{tasks[idx]['title']}\" oznaczone jako ukończone.")
        else:
            print("Nieprawidłowy numer.")
    except ValueError:
        print("Wprowadź liczbę.")

# Główna pętla
while True:
    show_menu()
    choice = input("Wybierz opcję (1-5): ")
    
    if choice == '1':
        show_tasks()
    elif choice == '2':
        add_task()
    elif choice == '3':
        delete_task()
    elif choice == '4':
        mark_done()
    elif choice == '5':
        print("Do zobaczenia!")
        break
    else:
        print("Nieprawidłowy wybór. Spróbuj ponownie.")
import os

TODO_FILE = "todo.txt"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def show_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        print("\nYour To-Do List:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")
    print()

def add_task(tasks):
    task = input("Enter a new task: ")
    tasks.append(task)
    print("Task added.")

def delete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"Deleted: {removed}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def main():
    tasks = load_tasks()
    while True:
        print("\nMenu:\n1. Show Tasks\n2. Add Task\n3. Delete Task\n4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            show_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
