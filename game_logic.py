import time, random
from game_levels import letters, grid, positions
from utilities import clear_screen, is_valid, GameGrid
from termcolor import cprint

# next time na ako mag-aadd ng termcolor edits katamad pa di naman required
class WordscapesGame:
    '''
    Main game class that manages the Wordscapes puzzle game logic.
    
    This class handles all game mechanics including letter management,
    word guessing, scoring, grid updates, and game state tracking.
    '''

    def __init__(self, letters, grid, positions):
        '''
        Initialize a new WordscapesGame instance.
        
        ==========
        Parameters:
        ==========
        letters : list
            List of available letters for forming words
        grid : list
            2D grid representation of the puzzle
        positions : dict
            Dictionary mapping words to their grid positions
        '''

        self.letters = letters
        self.words = set(positions.keys())
        self.grid = GameGrid(grid, positions)
        self.positions = positions
        self.found_words = set()
        self.lives = 5
        self.points = 0
        self.last_guess = None
        
    def shuffle_letters(self):
        '''
        Randomly reorders the available letters.
        '''

        random.shuffle(self.letters)
    
    def calculate_points(self, guess, found_words):
        '''
        Calculates points earned for a correct guess.
        
        Points are awarded based on the number of new grid cells (letters)
        that are revealed by the current word that weren't already
        revealed by previously found words.

        ==========
        Parameters:
        ==========
        guess: str
            The correctly guessed word
        found_words: set
            Set of words already found by the player
        '''

        return len(set(self.positions[guess]) - \
            set(coordinate for word in found_words 
                for coordinate in self.positions[word]))

    def play(self, nickname):
        '''
        Main game loop that manages the gameplay flow.
        
        Continues until all words are found, lives run out,
        or player chooses to exit.

        ==========
        Parameters:
        ==========
        nickname: str
            Player's nickname for display purposes
        '''

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
        '''
        Displays the current game state information.
        
        Shows available letters, remaining lives, current score,
        words found, last correct guess, and available commands to the player.
        '''
        print('-'*75)
        print(f"🔠Available letters: {'-'.join(self.letters)}")
        print(f"❤️‍🔥 Lives: {self.lives}")
        print(f"🌟 Score: {self.points}") 
        print(f"📖 Words found: {len(self.found_words)}/{len(self.words)}")
        print(f"📝 Last correct guess: {self.last_guess}")
        print("🛠️ Commands: [shuffle] to shuffle letters, [exit] to quit")
        print('-'*75)

    def the_guess(self, guess):
        '''
        Processes a player's word guess.
        
        Validates the guess, updates game state based on correctness,
        and provides feedback to the player.
        
        ==========
        Parameters:
        ==========
        guess: str
            The player's word guess
        '''

        if is_valid(guess, ''.join(self.letters)):
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
        '''
        Displays the end game results.
        
        Shows all possible words, words found by the player, final score,
        and a victory or game over message depending on results.
        '''

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