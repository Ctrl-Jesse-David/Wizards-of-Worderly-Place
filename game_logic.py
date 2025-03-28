import os, time
from game_levels import letters, grid, positions
import random
player_nick = ""

def menu():
    global player_nick

    while True:
        print("\n" + "="*40)
        print("🧙 Welcome to Wizards of Worderly Place!".center(40))
        print("="*40)
        print("\n1. 🎮 Start Game")
        print("2. 🚪 Exit")
        choice = input("\n👉 Enter your choice: ")

        if choice == "1":
            print("\n🎲 Starting the game...")
            time.sleep(0.25)
            if not player_nick:
                print("\n" + "-"*40)
                player_nick = input("👤 Enter your nickname: ")
            return True

        elif choice == "2":
            return False 

        else:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)

class GameGrid:
    def __init__(self, grid, positions):
        self.grid = grid
        self.positions = positions

    def refresh_display(self):
        return os.system('cls' if os.name == 'nt' else 'clear')
                         
    def display_grid(self):
        self.refresh_display()
        print(f'Welcome to Wizards of Worderly Place, {player_nick}!\n')
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
                break

            self.the_guess(guess)
            
        self.grid.refresh_display()
        self.grid.display_grid()
        self.end_game()
        return True #Means game is complete

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
            print('Game Over!\n')

def main():
    while True:  
        game = WordscapesGame(letters, grid, positions)
        game.play()
        
        while True:
            retry = input("\n🔄 Would you like to play again? [y/n]: ").lower().strip()
            if retry in ['y', 'n']:
                time.sleep(0.25)
                break
            else:
                print("baliw ka ba. Please enter 'y' or 'n'.")
        
        if retry == 'n':
            print("\nReturning to main menu...")
            time.sleep(0.5)
            break

if __name__ == "__main__":
    while True:
        game_start = menu()
        if game_start:
            main()

        else:
            time.sleep(0.25)
            print("Exiting the game...")
            break