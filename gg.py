import random
import time

def intro():
    print("Witaj w grze 'Zgadnij liczbę'!")
    print("Mam na myśli liczbę od 1 do 100.")
    print("Spróbuj ją odgadnąć w jak najmniejszej liczbie prób.\n")

def get_player_name():
    name = input("Podaj swoje imię: ")
    return name.strip().capitalize()

def get_guess():
    while True:
        try:
            guess = int(input("Zgadnij liczbę: "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("Liczba musi być w przedziale 1-100.")
        except ValueError:
            print("To nie jest liczba!")

def play_game(name):
    number = random.randint(1, 100)
    attempts = 0
    print("\nRozpoczynamy zgadywanie!\n")

    while True:
        guess = get_guess()
        attempts += 1

        if guess < number:
            print("Za mało!")
        elif guess > number:
            print("Za dużo!")
        else:
            print(f"Brawo, {name}! Odgadłeś liczbę w {attempts} próbach.")
            save_score(name, attempts)
            break

def save_score(name, attempts):
    with open("wyniki.txt", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {name}: {attempts} prób\n")

def show_scores():
    print("\n--- Historia wyników ---")
    try:
        with open("wyniki.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Brak zapisanych wyników.")

def main():
    intro()
    name = get_player_name()
    play_game(name)
    show_scores()

if __name__ == "__main__":
    main()
