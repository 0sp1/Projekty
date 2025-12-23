import json
import os
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
        self.show_reminders()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.tasks = json.load(f)
                    for t in self.tasks:
                        t.setdefault("tags", [])
                        t.setdefault("recurring", None)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def show_reminders(self):
        today = datetime.today().date()
        found = False

        for t in self.tasks:
            if t["completed"]:
                continue
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if due < today:
                print(f"OVERDUE: {t['description']} (due {t['due_date']})")
                found = True
            elif due == today:
                print(f"DUE TODAY: {t['description']}")
                found = True

        if not found:
            print("No reminders.")

    def add_task(self, desc, priority, due, tags, recurring):
        self.tasks.append({
            "description": desc,
            "completed": False,
            "priority": priority,
            "due_date": due,
            "tags": tags,
            "recurring": recurring
        })
        self.save_tasks()
        print("Task added.")

    def view_tasks(self, tasks=None):
        tasks = tasks if tasks is not None else self.tasks
        if not tasks:
            print("No tasks.")
            return

        today = datetime.today().date()

        for i, t in enumerate(tasks, 1):
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            overdue = "OVERDUE" if not t["completed"] and due < today else ""
            tags = ", ".join(t["tags"]) if t["tags"] else "None"
            recur = t["recurring"] if t["recurring"] else "No"

            print(
                f"{i}. {t['description']} "
                f"[{'Done' if t['completed'] else 'Pending'}] | "
                f"Priority: {t['priority']} | Due: {t['due_date']} | "
                f"Tags: {tags} | Recurring: {recur} {overdue}"
            )

    def complete_task(self, i):
        if 0 <= i < len(self.tasks):
            task = self.tasks[i]
            if task["recurring"]:
                self.advance_recurring(task)
                print("Recurring task advanced.")
            else:
                task["completed"] = True
                print("Task completed.")
            self.save_tasks()

    def advance_recurring(self, task):
        due = datetime.strptime(task["due_date"], "%Y-%m-%d")
        if task["recurring"] == "daily":
            due += timedelta(days=1)
        elif task["recurring"] == "weekly":
            due += timedelta(days=7)
        elif task["recurring"] == "monthly":
            due += timedelta(days=30)
        task["due_date"] = due.strftime("%Y-%m-%d")

    def delete_task(self, i):
        if 0 <= i < len(self.tasks):
            print(f"Deleted: {self.tasks[i]['description']}")
            self.tasks.pop(i)
            self.save_tasks()

    def search(self, keyword):
        self.view_tasks([
            t for t in self.tasks
            if keyword.lower() in t["description"].lower()
        ])

    def filter_tasks(self, mode):
        today = datetime.today().date()
        out = []

        for t in self.tasks:
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if mode == "completed" and t["completed"]:
                out.append(t)
            elif mode == "pending" and not t["completed"]:
                out.append(t)
            elif mode == "overdue" and not t["completed"] and due < today:
                out.append(t)
            elif mode in ("low", "medium", "high") and t["priority"].lower() == mode:
                out.append(t)

        self.view_tasks(out)

    def filter_by_tag(self, tag):
        self.view_tasks([
            t for t in self.tasks
            if tag.lower() in [x.lower() for x in t["tags"]]
        ])

    def sort_tasks(self, mode):
        if mode == "date":
            tasks = sorted(self.tasks, key=lambda t: t["due_date"])
        elif mode == "priority":
            order = {"Low": 1, "Medium": 2, "High": 3}
            tasks = sorted(self.tasks, key=lambda t: order[t["priority"]], reverse=True)
        else:
            print("Invalid sort.")
            return
        self.view_tasks(tasks)

    def stats(self):
        total = len(self.tasks)
        completed = sum(t["completed"] for t in self.tasks)
        overdue = sum(
            1 for t in self.tasks
            if not t["completed"] and
            datetime.strptime(t["due_date"], "%Y-%m-%d").date() < datetime.today().date()
        )

        print("Statistics")
        print(f"Total     : {total}")
        print(f"Completed : {completed}")
        print(f"Pending   : {total - completed}")
        print(f"Overdue   : {overdue}")
        if total:
            print(f"Progress  : {(completed / total) * 100:.1f}%")

def main():
    tm = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. View")
        print("2. Add")
        print("3. Complete")
        print("4. Delete")
        print("5. Search")
        print("6. Filter")
        print("7. Filter by tag")
        print("8. Sort")
        print("9. Statistics")
        print("10. Exit")

        c = input("Choose: ")

        if c == "1":
            tm.view_tasks()

        elif c == "2":
            d = input("Description: ")
            p = input("Priority (Low/Medium/High): ").capitalize()
            due = input("Due (YYYY-MM-DD): ")
            tags = [t.strip() for t in input("Tags (comma): ").split(",") if t.strip()]
            r = input("Recurring (daily/weekly/monthly/none): ").lower()
            r = r if r in ("daily", "weekly", "monthly") else None
            tm.add_task(d, p, due, tags, r)

        elif c == "3":
            tm.view_tasks()
            tm.complete_task(int(input("Task #: ")) - 1)

        elif c == "4":
            tm.view_tasks()
            tm.delete_task(int(input("Task #: ")) - 1)

        elif c == "5":
            tm.search(input("Keyword: "))

        elif c == "6":
            tm.filter_tasks(input("completed / pending / overdue / low / medium / high: "))

        elif c == "7":
            tm.filter_by_tag(input("Tag: "))

        elif c == "8":
            tm.sort_tasks(input("date / priority: "))

        elif c == "9":
            tm.stats()

        elif c == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
