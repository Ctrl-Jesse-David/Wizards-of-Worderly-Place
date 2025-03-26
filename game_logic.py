import os, time
from game_levels import letters, words, grid, positions
import random

class GameGrid:
    def __init__(self, grid, positions):
        self.grid = grid
        self.positions = positions

    def refresh_display(self):
        return os.system('cls' if os.name == 'nt' else 'clear')
                         
    def display_grid(self):
        self.refresh_display()
        print('WELCOME TO WORDSCAPES\n')
        for row in self.grid:
            print('  '.join(row))
        print('\n')

    def update_grid(self, word):
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                self.grid[row][col] = word[idx]
            return True
        return False


class WordscapesGame:
    def __init__(self, letters, words, grid, positions):
        self.letters = letters
        self.words = words
        self.grid = GameGrid(grid, positions)
        self.positions = positions
        self.found_words = set()
    
    def shuffle_letters(self):
        list_letters = list(self.letters)
        random.shuffle(list_letters)
        self.letters = ''.join(list_letters)

    def is_valid(self, guess):
        return all(guess.count(letter) <= self.letters.count(letter) 
                   for letter in guess)

    def play(self):
        while self.words != self.found_words:
            self.grid.display_grid()
            print(f"Available letters: {self.letters}")
            print("Commands: [shuffle] to shuffle letters, [exit] to quit\n")

            guess = input('Guess a word: ').upper()

            if guess == 'SHUFFLE':
                self.shuffle_letters()
                continue
            
            elif guess == 'EXIT':
                time.sleep(0.5)
                break

            elif guess in self.words:
                if guess in self.found_words:
                    print('Word has already been found')
                    time.sleep(0.85)
                
                elif self.is_valid(guess):
                    self.found_words.add(guess)
                    self.grid.update_grid(guess)
                    print('Correct!')
                    time.sleep(0.85)
                    
                else:
                    print('invalid Word')
                    time.sleep(0.85)

            else:
                print('Word not in list')
            print('Press enter to continue...')

        self.grid.display_grid()

        if self.words == self.found_words:
            print('Congratulations! You guessed all the words.')
        else:
            print('Thank you for playing!\n')

            

if __name__ == "__main__":
    game = WordscapesGame(letters, words, grid, positions)
    game.play()