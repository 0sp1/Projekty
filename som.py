import random

rooms = {
    "start": {"desc": "You are in a small room. There is a door to the north.", "north": "hall"},
    "hall": {"desc": "A long hallway with doors east and west.", "east": "treasure", "west": "trap", "south": "start"},
    "treasure": {"desc": "You found a shiny treasure chest! You win!", "end": True},
    "trap": {"desc": "Oh no! It's a trap room. You lose!", "end": True}
}

def move(current, direction):
    if direction in rooms[current]:
        return rooms[current][direction]
    else:
        print("You can't go that way.")
        return current

def play():
    current_room = "start"
    while True:
        print("\n" + rooms[current_room]["desc"])
        if "end" in rooms[current_room]:
            break
        direction = input("Which way do you go? ").lower()
        current_room = move(current_room, direction)

def main():
    print("=== Mini Text Adventure ===")
    while True:
        play()
        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
