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
        for t in self.tasks:
            if t["completed"]:
                continue
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if due < today:
                print(f"OVERDUE: {t['description']} (due {t['due_date']})")
            elif due == today:
                print(f"DUE TODAY: {t['description']}")

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

    def duplicate_task(self, i, new_due):
        if 0 <= i < len(self.tasks):
            t = self.tasks[i]
            self.tasks.append({
                "description": t["description"],
                "completed": False,
                "priority": t["priority"],
                "due_date": new_due,
                "tags": list(t["tags"]),
                "recurring": t["recurring"]
            })
            self.save_tasks()

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
            status = "Done" if t["completed"] else "Pending"

            print(
                f"{i}. {t['description']} [{status}] | "
                f"Priority: {t['priority']} | Due: {t['due_date']} | "
                f"Tags: {tags} | Recurring: {recur} {overdue}"
            )

    def complete_task(self, i):
        if 0 <= i < len(self.tasks):
            t = self.tasks[i]
            if t["recurring"]:
                self.advance_recurring(t)
            else:
                t["completed"] = True
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

    def snooze_task(self, i, days):
        if 0 <= i < len(self.tasks):
            due = datetime.strptime(self.tasks[i]["due_date"], "%Y-%m-%d")
            due += timedelta(days=days)
            self.tasks[i]["due_date"] = due.strftime("%Y-%m-%d")
            self.save_tasks()

    def delete_task(self, i):
        if 0 <= i < len(self.tasks):
            self.tasks.pop(i)
            self.save_tasks()

    def archive_completed(self):
        archived = self.load_archive()
        remaining = []
        for t in self.tasks:
            if t["completed"]:
                archived.append(t)
            else:
                remaining.append(t)
        self.tasks = remaining
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
        if mode == "date":
            self.view_tasks(sorted(self.tasks, key=lambda t: t["due_date"]))
        elif mode == "priority":
            order = {"Low": 1, "Medium": 2, "High": 3}
            self.view_tasks(sorted(self.tasks, key=lambda t: order[t["priority"]], reverse=True))

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
            w = csv.writer(f)
            w.writerow(["Description", "Completed", "Priority", "Due Date", "Tags", "Recurring"])
            for t in self.tasks:
                w.writerow([
                    t["description"], t["completed"], t["priority"],
                    t["due_date"], ", ".join(t["tags"]), t["recurring"] or ""
                ])

    def import_from_csv(self, filename):
        if not os.path.exists(filename):
            print("File not found.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tasks.append({
                    "description": row["Description"],
                    "completed": row["Completed"].lower() == "true",
                    "priority": row["Priority"],
                    "due_date": row["Due Date"],
                    "tags": [t.strip() for t in row["Tags"].split(",") if t.strip()],
                    "recurring": row["Recurring"] or None
                })
        self.save_tasks()

def main():
    tm = TaskManager()

    while True:
        print("\n1 View  2 Add  3 Complete  4 Delete  5 Edit")
        print("6 Search  7 Filter  8 Tag Filter  9 Sort")
        print("10 Stats  11 Export  12 Import")
        print("13 Archive  14 View Archive  15 Snooze  16 Duplicate  17 Exit")

        c = input("Choose: ")

        if c == "1":
            tm.view_tasks()
        elif c == "2":
            tm.add_task(
                input("Desc: "),
                input("Priority: ").capitalize(),
                input("Due (YYYY-MM-DD): "),
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
                input("Due (YYYY-MM-DD): "),
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
            tm.import_from_csv(input("CSV file: "))
        elif c == "13":
            tm.archive_completed()
        elif c == "14":
            tm.view_archive()
        elif c == "15":
            tm.view_tasks()
            tm.snooze_task(int(input("Task #: ")) - 1, int(input("Snooze days: ")))
        elif c == "16":
            tm.view_tasks()
            tm.duplicate_task(
                int(input("Task #: ")) - 1,
                input("New due date (YYYY-MM-DD): ")
            )
        elif c == "17":
            break

if __name__ == "__main__":
    main()
