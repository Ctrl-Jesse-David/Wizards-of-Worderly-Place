import random
from utilities import is_valid

'''
if wala ka pang nagagawa na random 6 letter word generator
and valid words galing sa dictionary ni sir i made one:
'''

def get_main_and_valid_words(file_path):
    def _get_main_and_valid_words(file_path):
            chosen_word = None
            count = 0
            try:
                with open(file_path, 'r') as file:
                    for word in map(str.strip, file):
                        if len(word) == 6:
                            count += 1
                            if random.randint(1, count) == 1:
                                chosen_word = word
            except FileNotFoundError:
                print("dapat nanjan ung file")

            def get_valid_words(base_word):
                valid_words = []
                try:
                    with open(file_path, 'r') as file:
                        for word in map(str.strip, file):
                            if is_valid(word, base_word) and word != base_word:
                                valid_words.append(word)
                except FileNotFoundError:
                    print("bat wala yung file")

                return valid_words
            return [chosen_word, get_valid_words(chosen_word)]
    while True:
        main, valid_words = _get_main_and_valid_words(file_path)
        if len(valid_words) < 20:
            continue
        else:
            break
    return [main, valid_words]

print(get_main_and_valid_words("word_dictionary.txt"))

# di ko gets yung main_diagonal pero if 
# pwede siya on all parts of the grid ganito code ko

def main_diagonal_generator(word, grid):
    step = 2

    rand_x = random.randint(0, 4)
    rand_y = random.randint(0, 14)

    for i, letter in enumerate(word):
        grid[rand_x + i * step][rand_y + i * step] = letter

    return grid

grid = [['.' for _ in range(25)] for _ in range(15)]
updated_grid = main_diagonal_generator('streak', grid)

for row in updated_grid:
    print(' '.join(row))