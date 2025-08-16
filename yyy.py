import random
import time

# Quiz questions and answers
questions = {
    "What is the capital of France? ": "paris",
    "What is 5 * 6? ": "30",
    "Who wrote 'Hamlet'? ": "shakespeare",
    "What is the boiling point of water (°C)? ": "100",
    "Which planet is known as the Red Planet? ": "mars",
    "What is the largest mammal? ": "blue whale",
    "Who painted the Mona Lisa? ": "da vinci",
    "What language is spoken in Brazil? ": "portuguese",
    "What is the square root of 64? ": "8",
    "Which gas do humans need to breathe? ": "oxygen"
}

def ask_question(q, answer):
    """Ask a single question and return if correct."""
    user_answer = input(q).strip().lower()
    if user_answer == answer:
        print("✅ Correct!\n")
        return True
    else:
        print(f"❌ Wrong! The answer was: {answer}\n")
        return False

def quiz_game():
    print("🎉 Welcome to the Python Quiz Game! 🎉")
    print("You will be asked random questions. Let's see how many you can answer!\n")
    time.sleep(1)

    score = 0
    total = 5   # number of questions to ask
    asked = random.sample(list(questions.items()), total)

    for q, a in asked:
        if ask_question(q, a):
            score += 1
        time.sleep(0.5)

    print("🎯 Quiz Over! 🎯")
    print(f"Your final score: {score}/{total}")

    if score == total:
        print("🏆 Excellent! You nailed it all!")
    elif score >= total // 2:
        print("👍 Good job! You got more than half right.")
    else:
        print("😅 Better luck next time!")

if __name__ == "__main__":
    quiz_game()
