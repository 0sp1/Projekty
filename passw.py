import string, random
char = []
pwd = ""

passward_lenght = int(input("Lenght? "))
letter = input("Letters? ") == "y"
numbers = input("Numbers? ") == "y"
punctuation = input("punctuation? ") == "y"

if letter:
    char.extend(string.ascii_letters)
if numbers:
    char.extend(string.digits)
if punctuation:
    char.extend(string.punctuation)

for _ in range(passward_lenght):
    pwd += random.choice(char)
print(pwd)