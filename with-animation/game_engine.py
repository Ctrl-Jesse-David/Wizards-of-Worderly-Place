from display_manager import clear_screen, display_border, display_body, ansi_escape
from file_operations import update_leaderboard
from word_utils import is_valid
import random, time
from grid_renderer import GameGrid
from user_progress import get_user_stats
import user_progress
from termcolor import colored, cprint

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
        self.lives = int(len(self.words) * .4)
        self.points = 0
        self.last_guess = None
        self.free_hints = 5
        self.bought_hints = get_user_stats().get("hints_available", 0)
    
    def shuffle_letters(self, nickname):
        '''
        Randomly reorders the available letters.
        '''
        clear_screen()
        self.grid.display_grid(nickname, "white", "on_cyan")
        self.cur_state("white", "on_cyan")
        random.shuffle(self.letters)
        time.sleep(0.35)
    
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

    def get_hint(self, nickname):
        '''
        Reveals a random unrevealed letter, using free hints first then purchased.
        '''
        #Determine source

        if self.free_hints > 0:
            self.free_hints -= 1
            source = "free"
        else:
            import user_progress
            if self.bought_hints > 0 and user_progress.use_hint():
                self.bought_hints -= 1
                source = "purchased"
            else:
                clear_screen()
                self.grid.display_grid(nickname, "white", "on_red")
                self.cur_state("white", "on_red")
                cprint("No hints remaining!", "red", attrs=["bold"])
                time.sleep(0.5)
                return False

        #Gather hidden positions
        all_positions = {pos for w in self.words for pos in self.positions[w]}
        revealed_positions = {pos for w in self.found_words for pos in self.positions[w]}
        hidden_positions = list(all_positions - revealed_positions)

        if not hidden_positions:
            clear_screen()
            self.grid.display_grid(nickname, "white", "on_yellow")
            self.cur_state("white", "on_yellow")
            cprint("No hidden letters to reveal!", "yellow", attrs=["bold"])
            time.sleep(0.5)
            return False

        #Reveal letter
        row, col = random.choice(hidden_positions)
        for word, poses in self.positions.items():
            if (row, col) in poses:
                idx = poses.index((row, col))
                self.grid.incomplete_grid[row][col] = word[idx]
                break
        
        clear_screen()
        self.grid.display_grid(nickname, "white", "on_blue")
        self.cur_state("white", "on_blue")
        cprint(
            f"Hint used! ({source})  –  Free left: {self.free_hints}, Extra left: {self.bought_hints}",
            "blue", attrs=["bold"]
        )
        time.sleep(0.5)
        return True
    
    def get_retry_option(self, nickname, on_color):
        while True:
            self.grid.display_complete_grid(nickname, "white", on_color)
            self.end_game(on_color)
            print("")
            retry_option = input(colored("🔄 Would you like to play again?", attrs=["underline"]) 
                                            + colored(" [y/n]", attrs=["bold"]) + ": ")\
                                            .lower().strip()
            if retry_option in ['y', 'n']:
                return retry_option
            else:
                print('')
                cprint("Invalid response!", "red", attrs=["bold"])
                time.sleep(0.5)
                clear_screen()

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
            
            guess = input(colored("👉 Your Output: ", attrs=["bold"])).strip().upper()

            if guess in ['SHUFFLE', 'S']:
                self.shuffle_letters(nickname)
                continue
            
            elif guess in ['HINT', 'H']:
                self.get_hint(nickname)
                continue
            
            elif guess in ['EXIT', 'E']: 
                update_leaderboard(self.name, self.points)
                user_progress.update_score(self.points)
                self.grid.display_complete_grid(nickname)
                return self.get_retry_option(nickname, "on_red")

            self.the_guess(guess, nickname)
            
        clear_screen()

        # Determine the final outcome
        if len(self.found_words) == len(self.words):
            update_leaderboard(self.name, self.points)
            user_progress.update_score(self.points)
            return self.get_retry_option(nickname, "on_green")
            

        elif self.lives <= 0:
            return self.get_retry_option(nickname, "on_red")

        else:  # This covers if they exited early (EXIT/E)
            return self.get_retry_option(nickname, "on_red")


    def end_game(self, on_color):
        '''
        Displays the end game results.
        '''
        info = ['-'*75,
                '',
        *self.get_wrapped_words(colored("WORDS", attrs=["bold"]), self.words)]

        if self.found_words:
            info += self.get_wrapped_words(colored("FOUND WORDS", attrs=["bold"]), self.found_words)
        else:
            info.append(f"{colored("FOUND WORDS", attrs=["bold"])}: None")
            
        info += [""]
        info += [f"{colored('SCORE', attrs=["bold"])}: {self.points}", '', '-'*75]

        display_body(info, "white", on_color)
        
        if len(self.found_words) == len(self.words):
            display_body([colored('Congratulations! You guessed all the words.', color="green", attrs=["bold"]), ''], "white", on_color)
        else:
            display_body(['',colored('Game Over!', "red", attrs=["bold"]), ''], "white", on_color)
        display_border(on_color)

    
    def cur_state(self, color="white", on_color="on_white"):
        '''
        Displays the current game state information.
        
        Shows available letters, remaining lives, current score,
        words found, last correct guess, and available commands to the player.
        '''
        info = [
            '='*75,
            "",
            f"🔠 {colored('Available letters:', attrs=['bold'])} {'-'.join(self.letters)}",
            f"🌱 {colored('Lives:', attrs=['bold'])} {self.lives}",
            f"🌟 {colored('Score:', attrs=['bold'])} {self.points}",
            f"💡 {colored('Hints – Free:', attrs=['bold'])} {self.free_hints}, Extra: {self.bought_hints}",
            f"📖 {colored('Words found:', attrs=['bold'])} {len(self.found_words)}/{len(self.words)}",
            f"📝 {colored('Last correct guess:', attrs=['bold'])} {self.last_guess}",
            f"🎮 {colored('Commands:', attrs=['bold'])} [shuffle|s], [hint|h], [exit|e]",
            ""
        ]
        display_body(info, color, on_color)
        display_border(on_color)
        print("")

    def the_guess(self, guess, nickname):
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
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_green")
                    self.cur_state("white", "on_green")
                    cprint('Correct!', "green", attrs=["bold"])
                    
                    

                elif guess in self.non_placed_words:
                    self.lives += 1
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_yellow")
                    self.cur_state("white", "on_yellow")
                    cprint('Word not found in the grid. Bonus life granted!', 'green', attrs=['bold'])
                    

                else:
                    self.lives -= 1
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_red")
                    self.cur_state("white", "on_red")
                    cprint('Incorrect.', "red", attrs=["bold"])
                    



            elif (guess in self.words or guess in self.non_placed_words) and guess in self.found_words:
                clear_screen()
                self.grid.display_grid(nickname, "white", "on_magenta")
                self.cur_state("white", "on_magenta")
                cprint('Word has already been found.', "red", attrs=["bold"])
                
               
            
            else:
                self.lives -= 1
                clear_screen()
                self.grid.display_grid(nickname, "white", "on_red")
                self.cur_state("white", "on_red")
                cprint('Incorrect.', "red", attrs=["bold"])
                
            

        else:
            clear_screen()
            self.grid.display_grid(nickname, "white", "on_red")
            self.cur_state("white", "on_red")
            cprint(f"Invalid word! Only {'-'.join(list(self.letters))} is allowed", "red", attrs=["bold"])
            self.lives -= 1
            

        time.sleep(0.5)

    def get_wrapped_words(self, label, word_list, width=73):
        words = sorted(word_list)
        prefix_visible_len = len(ansi_escape.sub('', f"{label}: "))
        prefix = f"{label}: "
        lines = []
        line = prefix
        for word in words:
            word_str = f"{word}, "
            if len(ansi_escape.sub('', line)) + len(word_str.rstrip()) > width:
                lines.append(line.rstrip(', '))
                line = " " * prefix_visible_len + word_str
            else:
                line += word_str
        if line.strip():
            lines.append(line.rstrip(', '))

        max_length = max(len(ansi_escape.sub('', l)) for l in lines)

        padded_lines = []
        for l in lines:
            visible_len = len(ansi_escape.sub('', l))
            padding = max_length - visible_len
            padded_lines.append(l + ' ' * padding)
        
        return padded_lines