from display_manager import clear_screen, display_border, display_body, ansi_escape
from file_operations import update_leaderboard
from word_utils import is_valid, get_player_input, get_wrapped_words
from grid_renderer import GameGrid
from user_progress import get_user_stats
import user_progress, random, time
from termcolor import colored, cprint

'''
Game Logic

This module implements the core game mechanics for Wizards of Worderly Place,
including word validation, scoring, and game state management.
'''

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
        self.found_non_placed_words = set()
        self.lives = int(len(self.words) * .4)
        self.points = 0
        self.last_guess = None
        self.free_hints = 5
        self.bought_hints = get_user_stats().get("hints_available", 0)
        self.revealed_letters = set()
    
    def shuffle_letters(self, nickname):
        '''
        Randomly reorders the available letters.
        '''
        clear_screen()
        self.grid.display_grid(nickname, "white", 'on_light_cyan')
        self.cur_state("white", 'on_light_cyan')
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
                self.grid.display_grid(nickname, "white", "on_light_red")
                self.cur_state("white", "on_light_red")
                cprint("No hints remaining!", "red", attrs=["bold"])
                time.sleep(0.75)
                return False

        #Gather hidden positions
        all_positions = {pos for w in self.words for pos in self.positions[w]}
        revealed_positions = {pos for w in self.found_words for pos in self.positions[w]}
        revealed_positions.update(self.revealed_letters)
        hidden_positions = list(all_positions - revealed_positions)

        if not hidden_positions:
            clear_screen()
            self.grid.display_grid(nickname, "white", "on_light_yellow")
            self.cur_state("white", "on_light_yellow")
            cprint("No hidden letters to reveal!", 'light_yellow', attrs=["bold"])
            time.sleep(0.75)
            return False

        #Reveal letter
        row, col = random.choice(hidden_positions)
        self.revealed_letters.add((row, col)) 
        for word, poses in self.positions.items():
            if (row, col) in poses:
                idx = poses.index((row, col))
                if (row, col) in [(2 + i*2, 7 + i*2) for i in range(6)]:
                    self.grid.incomplete_grid[row][col] = colored(word[idx], 'light_blue', attrs=["bold"])
                else:
                    self.grid.incomplete_grid[row][col] = colored(word[idx], "magenta", attrs=["bold"])
                break
        
        clear_screen()
        self.grid.display_grid(nickname, "white", "on_magenta")
        self.cur_state("white", "on_magenta")
        cprint(
            f"Hint used! ({source})  -  Free left: {self.free_hints}, Extra left: {self.bought_hints}",
            "magenta", attrs=["bold"]
        )
        time.sleep(0.75)
        return True
    
    def get_retry_option(self, nickname, on_color, state):
        if state == "lost":
            color = 'light_red'
        else:
            color = 'green'
        while True:
            self.grid.display_grid(nickname, color, on_color)
            self.end_game(on_color)
            print("")
            
            cprint('🔄 Would you like to play again, exit, or view cheatsheet?', attrs=['bold'])
            print('')
            retry_option = input(
                f"👉 [{colored('Y', 'green', attrs=['bold'])}] {colored('Play', 'green', attrs=['bold'])} / "
                f"[{colored('N', 'light_red', attrs=['bold'])}] {colored('Exit', 'light_red', attrs=['bold'])} / "
                f"[{colored('C', 'light_cyan', attrs=['bold'])}] {colored('Cheatsheet', 'light_cyan', attrs=['bold'])}: "
            ).lower().strip()
            print('')

            if retry_option in ['y', 'n']:
                return retry_option
            
            elif retry_option == 'c':
                while True:
                    self.grid.display_complete_grid(nickname,'white', 'on_light_cyan')
                    self.end_game('on_light_cyan', 'cheat')
                    print('')
                    input()
                    break
                continue

            else:
                print('')
                cprint("🚫 Invalid response!", "red", attrs=["bold"])
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
            
            guess = get_player_input()

            if guess in ['-SHUFFLE', '-S', 'S']:
                self.shuffle_letters(nickname)
                continue
            
            elif guess in ['-HINT', '-H', 'H']:
                self.get_hint(nickname)
                continue
            
            elif guess in ['-EXIT', '-E', 'E']: 
                update_leaderboard(self.name, self.points)
                user_progress.update_score(self.points)
                return self.get_retry_option(nickname, "on_light_red", 'lost')

            self.the_guess(guess, nickname)
            
        clear_screen()

        if len(self.found_words) == len(self.words):
            update_leaderboard(self.name, self.points)
            user_progress.update_score(self.points)
            return self.get_retry_option(nickname, "on_green", 'win')
            

        elif self.lives <= 0:
            return self.get_retry_option(nickname, "on_light_red", 'lost')

        else:
            return self.get_retry_option(nickname, "on_light_red", 'lost')

    def end_game(self, on_color, state="none"):
        """
        Displays the end game results.
        """

        border = '-'*75
        info = [
            border,
            '',
            f"🌟 {colored('SCORE:', attrs=['bold'])} {self.points}   🌱 {colored('LIVES:', attrs=['bold'])} {self.lives}   📝 {colored('LAST GUESS:', attrs=['bold'])} {self.last_guess}",
            '',
            border,
            '',
            *get_wrapped_words(colored('WORDS', attrs=['bold']), self.words),
            '',
            '='*75
        ]

        display_body(info, "white", on_color)

        if state == "cheat":
            message = colored(f"Press {colored('Enter', 'light_cyan')} to return...", attrs=['bold'])

        else:
            if len(self.found_words) == len(self.words):
                message = colored('🎉 Congratulations! You guessed all the words. 🎉', 'green', attrs=['bold'])
            else:
                message = colored('💀 Game Over! 💀', 'light_red', attrs=['bold'])

        display_body(['', message, ''], "white", on_color)
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
            f"💡 {colored('Hints - Free:', attrs=['bold'])} {self.free_hints}, Extra: {self.bought_hints}",
            f"📖 {colored('Words found:', attrs=['bold'])} {len(self.found_words)}/{len(self.words)}",
            f"📝 {colored('Last correct guess:', attrs=['bold'])} {self.last_guess}",
            f"{self.words}",
            f"🎮 {colored('Commands:', attrs=['bold'])} " \
            f"[{colored('-shuffle', 'light_cyan', attrs=['bold'])}|{colored('-s', 'light_cyan', attrs=['bold'])}], " \
            f"[{colored('-hint', 'magenta', attrs=['bold'])}|{colored('-h', 'magenta', attrs=['bold'])}], " \
            f"[{colored('-exit', 'light_red', attrs=['bold'])}|{colored('-e', 'light_red', attrs=['bold'])}]",
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
            if guess not in self.found_words and guess not in self.found_non_placed_words:
                if guess in self.words:
                    self.grid.update_grid(guess)
                    self.last_guess = guess
                    self.found_words.add(guess)
                    points_earned = self.calculate_points(guess, self.found_words - {guess})
                    self.points += points_earned
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_green")
                    self.cur_state("white", "on_green")
                    cprint('✅ Correct!', "green", attrs=["bold"])
                    


                elif guess in self.non_placed_words:
                    self.lives += 1
                    self.found_non_placed_words.add(guess)
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_light_yellow")
                    self.cur_state("white", "on_light_yellow")
                    cprint('🧠 Word not found in the grid. Bonus life granted!', 'light_yellow', attrs=['bold'])
                    

                else:
                    self.lives -= 1
                    clear_screen()
                    self.grid.display_grid(nickname, "white", "on_light_red")
                    self.cur_state("white", "on_light_red")
                    cprint('🚫 Incorrect.', "red", attrs=["bold"])
                    
                    



            elif (guess in self.words and guess in self.found_words) or (guess in self.non_placed_words and self.found_non_placed_words):
                clear_screen()
                self.grid.display_grid(nickname, "white", "on_magenta")
                self.cur_state("white", "on_magenta")
                cprint('🔁 Word has already been found.', "magenta", attrs=["bold"])
                
               
            
            else:
                self.lives -= 1
                clear_screen()
                self.grid.display_grid(nickname, "white", "on_light_red")
                self.cur_state("white", "on_light_red")
                cprint('🚫 Incorrect.', "red", attrs=["bold"])
                
            

        else:
            clear_screen()
            self.grid.display_grid(nickname, "white", "on_light_red")
            self.cur_state("white", "on_light_red")
            cprint(f"🚫 Invalid word! Only {'-'.join(list(self.letters))} is allowed", "red", attrs=["bold"])
            self.lives -= 1
            
        print('')
        time.sleep(0.75)