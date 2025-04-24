import time, random
from utilities import clear_screen, is_valid, GameGrid
from termcolor import cprint, colored
from utilities import update_leaderboard

'''
Game Logic

This module implements the core game mechanics for Wizards of Worderly Place,
including word validation, scoring, and game state management.
'''

# next time na ako mag-aadd ng termcolor edits katamad pa di naman required
class WordscapesGame:
    '''
    Main game class that manages the Wordscapes puzzle game logic.
    
    This class handles all game mechanics including letter management,
    word guessing, scoring, grid updates, and game state tracking.
    '''

    def __init__(self, letters, incomplete_grid, positions, non_placed_words, complete_grid, name):
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
        self.grid = GameGrid(incomplete_grid, complete_grid, positions)
        self.positions = positions
        self.non_placed_words = non_placed_words
        self.complete_grid = complete_grid
        self.name = name
        self.found_words = set()
        self.lives = int(len(positions)*0.4) # 40% ??
        self.points = 0
        self.last_guess = None
        self.hints_remaining = int(len(positions)*0.2) # tentative na 30% lang ng num of words (or ibase ba natin sa num of letters sa grid)
        
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

    def get_hint(self):
        '''
        Reveals a random unrevealed letter in the grid.
        '''

        #No hints left
        if self.hints_remaining <= 0:
            cprint("No hints remaining!", "red", attrs=["bold"])
            time.sleep(1)
            return False
            
        #All unrevealed pos
        all_positions = set(pos for word in self.words for pos in self.positions[word])
        revealed_positions = set(pos for word in self.found_words for pos in self.positions[word])
        hidden_positions = list(all_positions - revealed_positions)
        
        if not hidden_positions:
            cprint("No hidden letters to reveal!", "yellow", attrs=["bold"])
            time.sleep(1)
            return False
            
        #Reveal random pos
        row, col = random.choice(hidden_positions)
        
        #Finds the letter and updates grid
        for word, positions in self.positions.items():
            if (row, col) in positions:
                letter_index = positions.index((row, col))
                self.grid.incomplete_grid[row][col] = word[letter_index]
                break
                
        self.hints_remaining -= 1
        cprint(f"Hint used! {self.hints_remaining} hints remaining.", "green", attrs=["bold"])
        time.sleep(1)
        return True

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

            if guess in ['SHUFFLE', 'S']:
                self.shuffle_letters()
                continue
            
            elif guess in ['HINT', 'H']:
                self.get_hint()
                continue
            
            elif guess in ['EXIT', 'E']: 
                update_leaderboard(self.name, self.points)
                self.grid.display_complete_grid(nickname)
                while True:
                    self.grid.display_complete_grid(nickname)
                    self.end_game()
                    retry_option = input("🔄 Would you like to play again? " 
                                    + colored("[y/n]", "blue", attrs=["bold"]) + ": ")\
                                    .lower().strip()
                    if retry_option in ['y', 'n']:
                        time.sleep(0.25)
                        return retry_option
                    else:
                        cprint("Invalid response!", "red", attrs=["bold"])
                        time.sleep(0.1)
                        clear_screen()

            self.the_guess(guess)
            
        clear_screen()
        if len(self.found_words) == len(self.words):
            self.grid.display_grid(nickname)
        else:
            self.grid.display_complete_grid(nickname)
        self.end_game()
        return

    def end_game(self):
        '''
        Displays the end game results.
        
        Shows all possible words, words found by the player, final score,
        and a victory or game over message depending on results.
        '''

        print('-'*75)
        self.print_wrapped_words("WORDS", self.words)
        self.print_wrapped_words("FOUND WORDS", self.found_words) if self.found_words else print("FOUND WORDS: None")
        print(f"SCORE: {self.points}")
        print('-'*75)

        if len(self.found_words) == len(self.words):
            cprint('Congratulations! You guessed all the words.'.center(75), color="green", attrs=["bold"])
            print('-'*75)
        else:
            cprint('Game Over!'.center(75), "red", attrs=["bold"])
            print('-'*75)

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
        print(f"💡 Hints remaining: {self.hints_remaining}")
        print(f"📖 Words found: {len(self.found_words)}/{len(self.words)}")
        print(f"📝 Last correct guess: {self.last_guess}")
        print("🛠️ Commands: [shuffle|s] to shuffle letters, [hint|h] for a hint, [exit|e] to quit")
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
            if guess not in self.found_words:
                if guess in self.words:
                    self.grid.update_grid(guess)
                    self.last_guess = guess
                    self.points += self.calculate_points(guess, self.found_words)
                    self.found_words.add(guess)
                    cprint('Correct!', "green", attrs=["bold"])

                elif guess in self.non_placed_words:
                    self.lives += 1
                    cprint('Word not found in the grid. Bonus life granted!', 'green', attrs=['bold'])

            elif (guess in self.words or guess in self.non_placed_words) and guess in self.found_words:
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

    def print_wrapped_words(self, label, word_list, width=75):
        words = sorted(word_list)
        prefix = f"{label}: "
        line = prefix
        for word in words:
            word_str = f"{word}, "
            if len(line) + len(word_str.rstrip()) > width:
                print(line.rstrip(', '))
                line = " " * len(prefix) + word_str
            else:
                line += word_str
        if line.strip():
            print(line.rstrip(', '))
 

    