import os, time
from game_levels import letters, grid, positions
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
    def __init__(self, letters, grid, positions):
        self.letters = letters
        self.words = set(positions.keys())
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
    
    def calculate_points(self, guess, found_words):
        return len(set(self.positions[guess]) - \
            set(coordinate for word in found_words 
                for coordinate in self.positions[word]))

    def play(self):
        while self.found_words != self.words and self.lives > 0:

            self.grid.display_grid()
            self.cur_state()

            guess = input('\nGuess a word: ').upper()

            if guess == 'SHUFFLE':
                self.shuffle_letters()
                continue
            
            elif guess == 'EXIT': 
                # MAY BUGS ATA KAPAG NAGEEXIT - N
                # Anong bug cuh - D
                break

            self.the_guess(guess)
            
        self.grid.refresh_display()
        self.grid.display_grid()
        self.end_game()

    def cur_state(self):
        print(f"\nAvailable letters: {self.letters}")
        print(f"Lives: {self.lives}")
        print(f"Points: {self.points}") 
        print(f"Words found: {len(self.found_words)}/{len(self.words)}")
        print(f"Last guess: {self.last_guess}")
        print("Commands: [shuffle] to shuffle letters, [exit] to quit\n")

    def the_guess(self, guess):
        if self.is_valid(guess):
            if guess in self.words and guess not in self.found_words:
                self.grid.update_grid(guess)
                self.last_guess = guess
                self.points += self.calculate_points(guess, self.found_words)
                self.found_words.add(guess)
                print('Correct!')

            elif guess in self.words and guess in self.found_words:
                print('Word has already been found.')
            
            else:
                print('Incorrect.')

        else:
            print(f"Invalid word! Only {'-'.join(list(self.letters))} is allowed")
            self.lives -= 1
            time.sleep(1)
            return

        time.sleep(0.35)        

    def end_game(self):
        print(f"WORDS: {', '.join(self.words)}")
        print(f"FOUND WORDS: {', '.join(self.found_words) if self.found_words else None}") 
        print(f"SCORE: {self.points}\n")

        if len(self.found_words) == len(self.words):
            print('Congratulations! You guessed all the words.\n')
        else:
            print('Game Over! Thank you for playing!\n')


if __name__ == "__main__":
    game = WordscapesGame(letters, grid, positions)
    game.play()