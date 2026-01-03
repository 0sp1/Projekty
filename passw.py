class Room:
    def __init__(self, name, description, items=None, enemy=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.connections = {}
        self.locked_connections = set()
        self.enemy = enemy  # NEW: room enemy

    def connect(self, direction, room, locked=False):
        self.connections[direction] = room
        if locked:
            self.locked_connections.add(direction)

    def describe(self):
        print(f"\nYou are in {self.name}.")
        print(self.description)

        if self.items:
            print(f"You see: {', '.join(self.items)}")

        if self.enemy:
            print(f"There is a hostile {self.enemy['name']} here!")

        if self.connections:
            print("Exits:", ", ".join(self.connections.keys()))


class Game:
    def __init__(self):
        self.inventory = []
        self.player_health = 20       # NEW: player health
        self.setup_world()
        self.current_room = self.rooms["Hall"]

    def setup_world(self):
        self.rooms = {
            "Hall": Room("the Hall", "A grand hall with a dusty chandelier."),
            "Kitchen": Room("the Kitchen", "It smells of old food.", ["Key"]),
            "Library": Room("the Library", "Shelves of books tower above you.", ["Map"]),
            "Cellar": Room("the Cellar", "It's dark and damp. You feel uneasy.",
                           enemy={"name": "Rat", "health": 10, "damage": 3})  # NEW enemy
        }

        self.rooms["Hall"].connect("north", self.rooms["Kitchen"])
        self.rooms["Hall"].connect("east", self.rooms["Library"], locked=True)  # Puzzle lock
        self.rooms["Kitchen"].connect("south", self.rooms["Hall"])
        self.rooms["Library"].connect("west", self.rooms["Hall"])
        self.rooms["Kitchen"].connect("down", self.rooms["Cellar"], locked=True)  # Key lock
        self.rooms["Cellar"].connect("up", self.rooms["Kitchen"])

        self.riddle_answer = "shadow"  # NEW puzzle answer

    def unlock_connection(self, from_room, direction):
        if direction in from_room.locked_connections:
            from_room.locked_connections.remove(direction)
            print("You hear a click. That way is now unlocked.")
        else:
            print("Nothing happens.")

    # NEW: handle combat
    def attack_enemy(self):
        enemy = self.current_room.enemy
        if not enemy:
            print("There is nothing to attack here.")
            return

        print(f"You attack the {enemy['name']}!")
        enemy['health'] -= 5

        if enemy['health'] <= 0:
            print(f"You have defeated the {enemy['name']}!")
            self.current_room.enemy = None
            return

        # Enemy counterattacks
        print(f"The {enemy['name']} attacks you back!")
        self.player_health -= enemy['damage']
        print(f"You have {self.player_health} HP remaining.")

        if self.player_health <= 0:
            print("You have been defeated... Game over.")
            exit()

    # NEW: puzzle solving command
    def solve_puzzle(self):
        room = self.current_room
        if room.name != "the Library":
            print("There is no puzzle to solve here.")
            return

        print("A whisper asks: 'I follow you everywhere but never leave a trace. What am I?'")
        answer = input("Your answer: ").strip().lower()

        if answer == self.riddle_answer:
            print("The room seems to shift... A hidden lock clicks open.")
            self.unlock_connection(self.rooms["Hall"], "east")
        else:
            print("That is not the correct answer.")

    def play(self):
        print("Welcome to the Adventure Game!")
        print("Your HP:", self.player_health)

        while True:
            self.current_room.describe()
            command = input("\nWhat do you do? ").strip().lower()

            if command in ["quit", "exit"]:
                print("Thanks for playing!")
                break

            elif command.startswith("go "):
                direction = command.split()[1]
                if direction in self.current_room.connections:
                    if direction in self.current_room.locked_connections:
                        print("That way is locked.")
                    else:
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

            elif command.startswith("use "):
                item = command.split(" ", 1)[1]
                if item in self.inventory:
                    if item == "key" and self.current_room.name == "the Kitchen":
                        self.unlock_connection(self.current_room, "down")
                    else:
                        print(f"You try using the {item}, but nothing happens.")
                else:
                    print("You don't have that item.")

            elif command == "attack":
                self.attack_enemy()

            elif command == "solve":
                self.solve_puzzle()

            else:
                print("I don't understand that command.")


if __name__ == "__main__":
    game = Game()
    game.play()
