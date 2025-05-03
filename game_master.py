import random, copy, time
from grid_constructor import generate_positions_dict, generate_word_grid
from display_manager import clear_screen
from game_engine import WordscapesGame
from termcolor import cprint, colored
from user_progress import update_score
from animations import mystical_loading

def get_game_level(dictionary_file):
    grid_data, placed_words, non_placed_words = generate_word_grid(dictionary_file)
    letters = list(placed_words[0][0])
    random.shuffle(letters)

    game_grid = []
    for row in grid_data:
        game_row = []
        for cell in row:
            game_row.append(colored(cell, "dark_grey") if cell == colored('.', 'dark_grey') else colored('#', attrs=["bold"]))
        game_grid.append(game_row)
    
    positions_dict = generate_positions_dict(placed_words)

    return letters, game_grid, positions_dict, non_placed_words, grid_data


def initialize_game(letters, incomplete_grid, positions, name, non_placed_words, complete_grid):
    '''
    Initializes and manages a WoWP game session for the player.

    This function creates a new WordscapesGame instance and 
    handles the game flow. The player is prompted to either 
    play again or return to the main menu after each game.

    ==========
    Parameters:
    ==========
    letters: str
        The letters available for forming words in the game
    grid: list
        The puzzle grid structure to be filled with words
    positions: dict
        Mapping of word positions within the grid
    name: str
        Player's nickname for score tracking
    '''

    game = WordscapesGame(
        list(letters),
        copy.deepcopy(incomplete_grid),
        copy.deepcopy(positions),
        copy.deepcopy(non_placed_words),
        copy.deepcopy(complete_grid),
        copy.deepcopy(name)
    )

    retry_option = game.play(name)

    update_score(game.points)
    return retry_option


def start_game_session(dictionary_file, nickname): # create
    '''
    Manages a complete game session including nickname input,
    game initialization, and retry logic.
    '''

    clear_screen()
    #Run games until user opts out
    while True:
        # mystical_loading('FORGING SPELLS!', ' FORGING COMPLETE!', "green", "on_green")
        letters, incomplete_grid, positions, non_placed_words, complete_grid = get_game_level(dictionary_file)
        retry_option = initialize_game(
            letters, incomplete_grid, positions,
            nickname, non_placed_words, complete_grid
        )

        if retry_option:
            if retry_option.lower() == 'n':
                mystical_loading('CLOSING THE PORTAL...', '' , "magenta", "on_magenta")
                break
            elif retry_option.lower() == 'y':
                continue
            else:
                mystical_loading('CLOSING THE PORTAL...', '' , "magenta", "on_magenta")
                break
        else:
            print("")
            cprint("Returning to main menu...", "yellow", attrs=["bold"])
            time.sleep(1)
            clear_screen()
            break

