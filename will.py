import random

QUESTIONS = [
    ("What is the capital of France?", "paris"),
    ("What is 5 + 7?", "12"),
    ("Who wrote 'Romeo and Juliet'?", "shakespeare"),
    ("What is the largest planet in our solar system?", "jupiter"),
    ("What is the chemical symbol for water?", "h2o"),
    ("What is 9 * 9?", "81"),
    ("What is the capital of Japan?", "tokyo"),
    ("Who painted the Mona Lisa?", "da vinci"),
    ("What is the square root of 64?", "8"),
    ("What is the fastest land animal?", "cheetah")
]

def ask_question(question, answer):
    user_answer = input(question + " ").strip().lower()
    return user_answer == answer

def play_quiz():
    score = 0
    questions = random.sample(QUESTIONS, 5)  # Pick 5 random questions
    for q, a in questions:
        if ask_question(q, a):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {a}.")
    print(f"\nYou got {score} out of {len(questions)} right.")
    return score

def main():
    print("=== Welcome to the Quiz Game ===")
    high_score = 0

    while True:
        score = play_quiz()
        if score > high_score:
            high_score = score
            print("🎉 New high score!")
        print(f"High Score: {high_score}")

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()