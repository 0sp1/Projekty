# class Dog:
#     def __init__(self, name, age):
#         self.age = age
#         self.name = name
    
#     def get_name(self):
#         return self.name
    
#     def get_age(self):
#         return self.age

#     def add_one(self, x):
#         return x + 1
    
#     def set_age(self, age):
#         self.age = age

#     def bark(self):
#         print("bark")

# #print(d.get_name())
# d = Dog("Robert", 12)
# d.set_age(5)
# print(d.get_age())

# # d2 = Dog("Andrzej", 4)
# # print(d2.get_age())

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade #0 - 100
    
    def get_grade(self):
        return self.grade
    
class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False
    
    def get_average_grade(self):
        average_grade = 0
        for student in self.students:
            average_grade += student.get_grade()
        
        return average_grade / len(self.students)

s1 = Student("Cwel", 12, 95)
s2 = Student("Debil", 18, 14)
s3 = Student("JebanyDebil", 23, 30)
s4 = Student("Kutacz", 21, 55)

course = Course("Biologia", 3)
course.add_student(s1)
course.add_student(s2)
course.add_student(s3)
course.add_student(s4)

print(course.get_average_grade)