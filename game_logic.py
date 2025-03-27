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
        self.lives = 5
        self.points = 0
        self.last_guess = None
        
    def shuffle_letters(self):
        list_letters = list(self.letters)
        random.shuffle(list_letters)
        self.letters = ''.join(list_letters)

    def is_valid(self, guess):
        return all(guess.count(letter) <= self.letters.count(letter) 
                   for letter in guess)

    def play(self):
        while len(self.found_words) < len(self.words) and self.lives > 0:

            self.grid.display_grid()

            if self.words == self.found_words:
                break
            self.cur_state()

            guess = input('\nGuess a word: ').upper()

            if guess == 'SHUFFLE':
                self.shuffle_letters()
                continue
            
            elif guess == 'EXIT': #MAY BUGS ATA KAPAG NAGEEXIT
                time.sleep(0.35)
                break

            self.the_guess(guess)

        self.end_game()

    def cur_state(self):
        print(f"\nAvailable letters: {self.letters}")
        print(f"Lives: {self.lives}")
        print(f"Points: {self.points}") 
        print(f"Words found: {len(self.found_words)}/{len(self.words)}")
        print(f"Last guess: {self.last_guess}")
        print("Commands: [shuffle] to shuffle letters, [exit] to quit\n")

    def the_guess(self, guess):
        if guess in self.words and guess not in self.found_words:
            self.found_words.add(guess)
            self.grid.update_grid(guess)
            self.last_guess = guess
            self.points += 1 #PER NEW LETTER DISC DAPAT UNG POINTS PERO NEXT TIME NA
            print('Correct!')

        else:
            print('Invalid word')
            self.lives -= 1

        time.sleep(0.35)        

    def end_game(self):
        if len(self.found_words) == len(self.words):
            print('\nCongratulations! You guessed all the words.\n')
        else:
            print('Game Over! Thank you for playing!\n')

        print(f"Words: {self.words}")
        print(f"Found words: {self.found_words}")
        #REVISION KO PA SIGURO*

if __name__ == "__main__":
    game = WordscapesGame(letters, words, grid, positions)
    game.play()