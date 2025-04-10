from termcolor import cprint, colored
from utilities import clear_screen, display_header, update_leaderboard
from game_logic import WordscapesGame
import time, copy

def start_game(letters, grid, positions, name):
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

    # For creating a new grid
    while True:
        game = WordscapesGame(
            list(letters),
            copy.deepcopy(grid),
            copy.deepcopy(positions)
        )
        game.play(name)
        update_leaderboard(name, game.points)

        retry_option = input("🔄 Would you like to play again? " 
                        + colored("[y/n]", "blue", attrs=["bold"]) + ": ")\
                        .lower().strip()
        if retry_option in ['y', 'n']:
            time.sleep(0.25)
            return retry_option
        else:
            cprint("Invalid response!", "red", attrs=["bold"])
            time.sleep(0.1)
        



def display_instructions():
    
    
    cprint("🔮 Power-ups & Hints:", "light_red", attrs=["bold"])
    print("  🪄 Shuffle - Rearranges the given letters.")
    print("  🔍 Hint - Reveals one letter in a hidden word.") # maybe mag-add din tayo nito?
    print("  🔵 Extra Life - Given if you find a valid word not in the grid") # ito yung sa plus life feature
    print("-"*75)

    input(colored("Press Enter to return to the main menu.", "light_red", attrs=["bold"]))
    clear_screen()


def display_leaderboard():
    '''
    Displays the top 8 player scores from the leaderboard.

    This function reads player scores from 'leaderboard.txt', sorts them
    in descending order, and displays the top scores.
    '''

    display_header(
        title="🏆 LEADERBOARD 🏆",
        color="yellow"
    )
    try:
        with open("leaderboard.txt", "r") as file:
            scores = sorted((line.strip().split(": ") for line in file), 
                            key=lambda x: int(x[1]), reverse=True)[:8]
        if scores:
            for rank, (name, score) in enumerate(scores, start=1):
                print(f"{rank}. {name} - {score}")
        else:
            print("No scores yet! Play to be the first on the leaderboard!")

    except FileNotFoundError:
        print("No leaderboard found. Play the game to create one!")

    print("-"*75)
    input(colored("Press Enter to return to the main menu.", 'yellow', attrs=["bold"]))