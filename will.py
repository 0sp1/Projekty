import random

responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
    "how are you": ["I'm just code, but I'm functioning as expected!", "All systems go!"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
    "help": ["You can ask me about greetings, how I'm doing, or just say bye!"],
    "default": ["Sorry, I don't understand that.", "Can you rephrase?", "Hmm, interesting..."]
}

def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return random.choice(responses["default"])

def main():
    print("🤖 ChatBot: Hello! Type something to chat. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("🤖 ChatBot: Goodbye!")
            break
        response = get_response(user_input)
        print("🤖 ChatBot:", response)

if __name__ == "__main__":
    main()
