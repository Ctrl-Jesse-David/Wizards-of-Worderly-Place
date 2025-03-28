import time, random
from game_levels import letters, grid, positions
from utilities import clear_screen, GameGrid
from termcolor import cprint

# next time na ako mag-aadd ng termcolor edits katamad pa di naman required
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

    def play(self, nickname):
        while self.found_words != self.words and self.lives > 0:

            self.grid.display_grid(nickname)
            self.cur_state()

            guess = input('Guess a word: ').upper()

            if guess == 'SHUFFLE':
                self.shuffle_letters()
                continue
            
            elif guess == 'EXIT': 
                break

            self.the_guess(guess)
            
        clear_screen()
        self.grid.display_grid(nickname)
        self.end_game()
        return

    def cur_state(self):
        print('-'*75)
        print(f"🔠Available letters: {self.letters}")
        print(f"❤️‍🔥 Lives: {self.lives}")
        print(f"🌟 Score: {self.points}") 
        print(f"📖 Words found: {len(self.found_words)}/{len(self.words)}")
        print(f"📝 Last guess: {self.last_guess}") # hindi to nag-uupdate pag mali yung guess (intentional ba to)
        print("🛠️ Commands: [shuffle] to shuffle letters, [exit] to quit")
        print('-'*75)

    def the_guess(self, guess):
        if self.is_valid(guess):
            if guess in self.words and guess not in self.found_words:
                self.grid.update_grid(guess)
                self.last_guess = guess
                self.points += self.calculate_points(guess, self.found_words)
                self.found_words.add(guess)
                cprint('Correct!', "green", attrs=["bold"])

            elif guess in self.words and guess in self.found_words:
                cprint('Word has already been found.', "red", attrs=["bold"])
            
            else:
                self.lives -= 1
                cprint('Incorrect.', "red", attrs=["bold"])

        else:
            cprint(f"Invalid word! Only {'-'.join(list(self.letters))} is allowed", "red", attrs=["bold"])
            self.lives -= 1
            time.sleep(1)
            return

        time.sleep(0.35)        

    def end_game(self):
        print('-'*75)
        print(f"WORDS: {', '.join(self.words)}")
        print(f"FOUND WORDS: {', '.join(self.found_words) if self.found_words else None}") 
        print(f"SCORE: {self.points}")
        print('-'*75)

        if len(self.found_words) == len(self.words):
            cprint('Congratulations! You guessed all the words.'.center(75), color="green", attrs=["bold"])
            print('-'*75)
        else:
            cprint('Game Over!'.center(75), "red", attrs=["bold"])
            print('-'*75)