import sys

history = []

def add(x, y): return x + y
def subtract(x, y): return x - y
def multiply(x, y): return x * y
def divide(x, y):
    if y == 0:
        print("❌ Cannot divide by zero.")
        return None
    return x / y

def show_menu():
    print("\n📱 Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Show History")
    print("6. Exit")

def get_numbers():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        return x, y
    except ValueError:
        print("⚠️ Invalid input.")
        return None, None

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == '6':
            print("👋 Goodbye!")
            sys.exit()

        elif choice == '5':
            if not history:
                print("🕘 No history yet.")
            else:
                print("\n🧾 History:")
                for entry in history:
                    print(entry)
            continue

        if choice not in {'1', '2', '3', '4'}:
            print("⚠️ Invalid choice.")
            continue

        x, y = get_numbers()
        if x is None or y is None:
            continue

        operations = {'1': add, '2': subtract, '3': multiply, '4': divide}
        op_symbols = {'1': '+', '2': '-', '3': '*', '4': '/'}
        result = operations[choice](x, y)

        if result is not None:
            record = f"{x} {op_symbols[choice]} {y} = {result}"
            print("✅", record)
            history.append(record)

if __name__ == "__main__":
    main()