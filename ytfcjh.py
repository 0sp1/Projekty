import sys

class Room:
    def __init__(self, name, description, items=None, exits=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.exits = exits if exits else {}

    def describe(self):
        print(f"\nYou are in the {self.name}.")
        print(self.description)
        if self.items:
            print("You see:", ", ".join(self.items))
        print("Exits:", ", ".join(self.exits.keys()))

class Game:
    def __init__(self):
        self.rooms = self.create_rooms()
        self.current_room = self.rooms["hall"]
        self.inventory = []

    def create_rooms(self):
        return {
            "hall": Room(
                "Hall",
                "A grand hall with a dusty chandelier.",
                items=["key"],
                exits={"north": "kitchen", "east": "library"}
            ),
            "kitchen": Room(
                "Kitchen",
                "The smell of old food lingers. You see a locked door.",
                exits={"south": "hall"}
            ),
            "library": Room(
                "Library",
                "Books line the shelves. A strange box sits on a table.",
                items=["note"],
                exits={"west": "hall"}
            ),
        }

    def play(self):
        print("Welcome to the Escape Game!")
        print("Type 'help' for commands.\n")

        while True:
            self.current_room.describe()
            command = input("\n> ").strip().lower()

            if command in ["quit", "exit"]:
                print("Goodbye!")
                sys.exit()
            elif command == "help":
                print("Commands: look, go [direction], take [item], inventory, quit")
            elif command.startswith("go "):
                self.move(command.split(" ", 1)[1])
            elif command.startswith("take "):
                self.take_item(command.split(" ", 1)[1])
            elif command == "look":
                self.current_room.describe()
            elif command == "inventory":
                print("You have:", ", ".join(self.inventory) if self.inventory else "Nothing")
            else:
                print("I don't understand that command.")

    def move(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.rooms[self.current_room.exits[direction]]
            if self.current_room.name == "Kitchen" and "key" in self.inventory:
                print("\nYou unlock the door and escape! You win!")
                sys.exit()
        else:
            print("You can't go that way.")

    def take_item(self, item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f"You picked up the {item}.")
        else:
            print("That item isn't here.")

if __name__ == "__main__":
    Game().play()
