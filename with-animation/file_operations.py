import sys
from random import choice
from word_utils import is_valid

def get_main_and_valid_words(file_path):
    def read_words():
        try:
            with open(file_path) as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            print(f"Error: Dictionary file '{file_path}' not found!")
            sys.exit(1)

    words = read_words()
    six_letter_words = [w for w in words if len(w) == 6]
    if not six_letter_words:
        return None

    main_word = choice(six_letter_words)
    valid_words = [w for w in words if 3 <= len(w) <= 6 and w != main_word and is_valid(w, main_word)]

    return (main_word, valid_words) if len(valid_words) >= 20 else get_main_and_valid_words(file_path)

def update_leaderboard(name, score):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name}: {score}\n")
