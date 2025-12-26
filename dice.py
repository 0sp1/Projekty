import json
import os
import csv
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self, filename="tasks.json", archive_file="archive.json"):
        self.filename = filename
        self.archive_file = archive_file
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

    def load_archive(self):
        if os.path.exists(self.archive_file):
            try:
                with open(self.archive_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_archive(self, archived):
        with open(self.archive_file, "w") as f:
            json.dump(archived, f, indent=4)

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

    def edit_task(self, i, desc, priority, due, tags, recurring):
        if 0 <= i < len(self.tasks):
            self.tasks[i].update({
                "description": desc,
                "priority": priority,
                "due_date": due,
                "tags": tags,
                "recurring": recurring
            })
            self.save_tasks()
            print("Task updated.")

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
            else:
                task["completed"] = True
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
            self.tasks.pop(i)
            self.save_tasks()

    def archive_completed(self):
        archived = self.load_archive()
        self.tasks, moved = [], self.tasks
        for t in moved:
            (archived if t["completed"] else self.tasks).append(t)
        self.save_tasks()
        self.save_archive(archived)

    def view_archive(self):
        self.view_tasks(self.load_archive())

    def search(self, keyword):
        self.view_tasks([t for t in self.tasks if keyword.lower() in t["description"].lower()])

    def filter_tasks(self, mode):
        today = datetime.today().date()
        self.view_tasks([
            t for t in self.tasks
            if (mode == "completed" and t["completed"]) or
               (mode == "pending" and not t["completed"]) or
               (mode == "overdue" and not t["completed"] and
                datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today) or
               (mode in ("low", "medium", "high") and t["priority"].lower() == mode)
        ])

    def filter_by_tag(self, tag):
        self.view_tasks([t for t in self.tasks if tag.lower() in map(str.lower, t["tags"])])

    def sort_tasks(self, mode):
        key = "due_date" if mode == "date" else None
        if mode == "priority":
            order = {"Low": 1, "Medium": 2, "High": 3}
            self.view_tasks(sorted(self.tasks, key=lambda t: order[t["priority"]], reverse=True))
        elif key:
            self.view_tasks(sorted(self.tasks, key=lambda t: t[key]))

    def stats(self):
        total = len(self.tasks)
        completed = sum(t["completed"] for t in self.tasks)
        overdue = sum(
            not t["completed"] and
            datetime.strptime(t["due_date"], "%Y-%m-%d").date() < datetime.today().date()
            for t in self.tasks
        )
        print(f"Total: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {total - completed}")
        print(f"Overdue: {overdue}")

    def export_to_csv(self, filename="tasks.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Description", "Completed", "Priority", "Due Date", "Tags", "Recurring"])
            for t in self.tasks:
                writer.writerow([
                    t["description"], t["completed"], t["priority"],
                    t["due_date"], ", ".join(t["tags"]), t["recurring"] or ""
                ])

def main():
    tm = TaskManager()

    while True:
        print("\n1 View  2 Add  3 Complete  4 Delete  5 Edit")
        print("6 Search  7 Filter  8 Tag Filter  9 Sort")
        print("10 Stats  11 Export  12 Archive  13 View Archive  14 Exit")

        c = input("Choose: ")

        if c == "1":
            tm.view_tasks()
        elif c == "2":
            tm.add_task(
                input("Desc: "),
                input("Priority: ").capitalize(),
                input("Due: "),
                [t.strip() for t in input("Tags: ").split(",") if t.strip()],
                input("Recurring: ").lower() or None
            )
        elif c == "3":
            tm.view_tasks()
            tm.complete_task(int(input("Task #: ")) - 1)
        elif c == "4":
            tm.view_tasks()
            tm.delete_task(int(input("Task #: ")) - 1)
        elif c == "5":
            tm.view_tasks()
            i = int(input("Task #: ")) - 1
            tm.edit_task(
                i,
                input("Desc: "),
                input("Priority: ").capitalize(),
                input("Due: "),
                [t.strip() for t in input("Tags: ").split(",") if t.strip()],
                input("Recurring: ").lower() or None
            )
        elif c == "6":
            tm.search(input("Keyword: "))
        elif c == "7":
            tm.filter_tasks(input("Mode: "))
        elif c == "8":
            tm.filter_by_tag(input("Tag: "))
        elif c == "9":
            tm.sort_tasks(input("date / priority: "))
        elif c == "10":
            tm.stats()
        elif c == "11":
            tm.export_to_csv()
        elif c == "12":
            tm.archive_completed()
        elif c == "13":
            tm.view_archive()
        elif c == "14":
            break

if __name__ == "__main__":
    main()
