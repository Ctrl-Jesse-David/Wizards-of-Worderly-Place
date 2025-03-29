from termcolor import cprint, colored
from utilities import clear_screen, display_header, update_leaderboard
from game_logic import WordscapesGame
import time, copy

def start_game(letters, grid, positions, name):
    while True:
        # para new grid each play
        game = WordscapesGame(
            list(letters),
            copy.deepcopy(grid),
            copy.deepcopy(positions)
        )
        game.play(name)

        while True:
            retry_option = input("🔄 Would you like to play again? " 
                            + colored("[y/n]", "blue", attrs=["bold"]) + ": ")\
                            .lower().strip()
            if retry_option in ['y', 'n']:
                time.sleep(0.25)
                break
            else:
                cprint("Invalid response!", "red", attrs=["bold"])
                time.sleep(0.1)
        
        update_leaderboard(name, game.points)

        if retry_option == 'n':
            print("Returning to main menu...")
            time.sleep(0.5)
            clear_screen()
            break
        else:
            print("Restarting the game...")
            time.sleep(0.6)
            continue



def display_instructions():
    display_header(
        title="📜 GAME INSTRUCTIONS 📜",
        color="light_red"
    )

    cprint("🕹️  How to Play:", "light_red", attrs=["bold"])
    print("  Form words using the given letters to solve the puzzle.")
    print("  Type the words and press Enter to submit your answer.")
    print("-"*75)
    
    cprint("✨ Game Rules:", "light_red", attrs=["bold"])
    print("  🏆 Find all possible words to complete the level.")
    print("  🚫 Invalid words or repeated words will not be accepted.")
    print("  💀 Choose your words wisely! You have limited lives.")
    print("-"*75)
    
    cprint("🔮 Power-ups & Hints:", "light_red", attrs=["bold"])
    print("  🪄 Shuffle - Rearranges the given letters.")
    print("  🔍 Hint - Reveals one letter in a hidden word.") # maybe mag-add din tayo nito?
    print("  🔵 Extra Life - Given if you find a valid word not in the grid") # ito yung sa plus life feature
    print("-"*75)

    input(colored("Press Enter to return to the main menu.", "light_red", attrs=["bold"]))
    clear_screen()


def display_leaderboard():
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