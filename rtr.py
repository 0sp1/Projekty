import string

def analyze_text(text):
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", ""))
    sentence_count = text.count(".") + text.count("!") + text.count("?")

    clean_text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    word_list = clean_text.split()

    freq = {}
    for word in word_list:
        freq[word] = freq.get(word, 0) + 1

    most_common = max(freq, key=freq.get) if freq else None

    avg_word_length = sum(len(word) for word in word_list) / word_count if word_count > 0 else 0

    reading_speed_wpm = 200
    reading_time_minutes = word_count / reading_speed_wpm
    reading_time_seconds = int(reading_time_minutes * 60)

    return {
        "Words": word_count,
        "Characters (with spaces)": char_count,
        "Characters (no spaces)": char_no_spaces,
        "Sentences": sentence_count,
        "Most Common Word": most_common,
        "Average Word Length": round(avg_word_length, 2),
        "Estimated Reading Time": f"{reading_time_minutes:.2f} minutes ({reading_time_seconds} seconds)"
    }

def main():
    print("Text Analyzer")
    while True:
        text = input("\nEnter text (or 'exit' to quit): ").strip()
        if text.lower() == "exit":
            print("Exiting Text Analyzer.")
            break

        results = analyze_text(text)
        for key, value in results.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
