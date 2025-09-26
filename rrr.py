import json
import os
import csv

class Student:
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = grades if grades else []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

    def to_dict(self):
        return {"name": self.name, "grades": self.grades}

    @staticmethod
    def from_dict(data):
        return Student(data["name"], data.get("grades", []))

class GradeBook:
    def __init__(self, filename="grades.json"):
        self.filename = filename
        self.students = []
        self.load()

    def add_student(self, name):
        self.students.append(Student(name))
        self.save()

    def add_grade(self, name, grade):
        for s in self.students:
            if s.name.lower() == name.lower():
                s.add_grade(grade)
                self.save()
                return
        print("Student not found.")

    def list_students(self):
        if not self.students:
            print("No students available.")
            return
        for s in self.students:
            avg = round(s.average(), 2)
            print(f"{s.name}: {s.grades} (Avg: {avg})")

    def rank_students(self):
        if not self.students:
            print("No students available.")
            return
        ranked = sorted(self.students, key=lambda s: s.average(), reverse=True)
        print("\nStudent Rankings:")
        for i, s in enumerate(ranked, 1):
            print(f"{i}. {s.name} - Avg: {round(s.average(), 2)}")

    def delete_student(self, name):
        before = len(self.students)
        self.students = [s for s in self.students if s.name.lower() != name.lower()]
        if len(self.students) < before:
            print(f"Deleted {name} from the grade book.")
            self.save()
        else:
            print("Student not found.")

    def export_csv(self, filename="grades.csv"):
        if not self.students:
            print("No students available to export.")
            return
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Grades", "Average"])
            for s in self.students:
                writer.writerow([s.name, ", ".join(map(str, s.grades)), round(s.average(), 2)])
        print(f"Exported data to {filename}")

    def import_csv(self, filename="grades.csv"):
        if not os.path.exists(filename):
            print("CSV file not found.")
            return
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            self.students = []
            for row in reader:
                grades = [float(g.strip()) for g in row["Grades"].split(",") if g.strip()]
                self.students.append(Student(row["Name"], grades))
        self.save()
        print(f"Imported data from {filename}")

    def save(self):
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]

def menu():
    gb = GradeBook()
    while True:
        print("\nGrade Book")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. List Students")
        print("4. Show Rankings")
        print("5. Delete Student")
        print("6. Export to CSV")
        print("7. Import from CSV")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter student name: ")
            gb.add_student(name)
        elif choice == "2":
            name = input("Enter student name: ")
            try:
                grade = float(input("Enter grade: "))
                gb.add_grade(name, grade)
            except ValueError:
                print("Invalid grade.")
        elif choice == "3":
            gb.list_students()
        elif choice == "4":
            gb.rank_students()
        elif choice == "5":
            name = input("Enter name of student to delete: ")
            gb.delete_student(name)
        elif choice == "6":
            gb.export_csv()
        elif choice == "7":
            gb.import_csv()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
