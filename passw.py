class Room:
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.connections = {}

    def connect(self, direction, room):
        self.connections[direction] = room

    def describe(self):
        print(f"\nYou are in {self.name}.")
        print(self.description)
        if self.items:
            print(f"You see: {', '.join(self.items)}")
        if self.connections:
            print("Exits:", ", ".join(self.connections.keys()))

class Game:
    def __init__(self):
        self.inventory = []
        self.setup_world()
        self.current_room = self.rooms["Hall"]

    def setup_world(self):
        self.rooms = {
            "Hall": Room("the Hall", "A grand hall with a dusty chandelier."),
            "Kitchen": Room("the Kitchen", "It smells of old food.", ["Key"]),
            "Library": Room("the Library", "Shelves of books tower above you.", ["Map"]),
            "Cellar": Room("the Cellar", "It's dark and damp. You feel uneasy.")
        }
        self.rooms["Hall"].connect("north", self.rooms["Kitchen"])
        self.rooms["Hall"].connect("east", self.rooms["Library"])
        self.rooms["Kitchen"].connect("south", self.rooms["Hall"])
        self.rooms["Library"].connect("west", self.rooms["Hall"])
        self.rooms["Kitchen"].connect("down", self.rooms["Cellar"])
        self.rooms["Cellar"].connect("up", self.rooms["Kitchen"])

    def play(self):
        print("Welcome to the Adventure Game!")
        while True:
            self.current_room.describe()
            command = input("\nWhat do you do? ").strip().lower()

            if command in ["quit", "exit"]:
                print("Thanks for playing!")
                break
            elif command.startswith("go "):
                direction = command.split()[1]
                if direction in self.current_room.connections:
                    self.current_room = self.current_room.connections[direction]
                else:
                    print("You can't go that way.")
            elif command.startswith("take "):
                item = command.split(" ", 1)[1]
                if item in self.current_room.items:
                    self.inventory.append(item)
                    self.current_room.items.remove(item)
                    print(f"You picked up {item}.")
                else:
                    print("That item isn't here.")
            elif command == "inventory":
                print("You have:", ", ".join(self.inventory) if self.inventory else "Nothing")
            else:
                print("I don't understand that command.")

if __name__ == "__main__":
    game = Game()
    game.play()
