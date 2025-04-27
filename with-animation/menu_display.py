from display_manager import display_header, clear_screen, display_footer
from termcolor import cprint, colored
from user_progress import current_user, get_user_stats, login_user, display_user_profile, display_shop

'''
Options

This module handles the game's menu options and player interactions for Wizards of Worderly Place.
It manages game sessions, displays instructions, and maintains the leaderboard system.
'''

def display_main_menu():
    '''
    Displays the main menu interface of the game.
    
    This function presents a formatted menu showing the game title
    and available options including starting the game, viewing instructions,
    checking the leaderboard, and exiting the game.
    '''

    display_header(
            title="🧙 Welcome to Wizards of Worderly Place! 🧙",
            color="light_blue"
        )
    print("Can you uncover all the hidden words?".center(75))
    print("Test your wits and master the art of wordplay!".center(75))
    print("-" * 75)

    if current_user:
        stats = get_user_stats()
        print(f"Logged in as: {stats['nickname']} | Points: {stats['points']} | Hints: {stats['hints_available']}".center(75))
        print("-" * 75)

    menu_options = [
    " " * 11 + "📖  " + colored("[S]", "light_blue", attrs=["bold"]) + "  Start Game   📖",
    " " * 11 + "📜  " + colored("[I]", "light_blue", attrs=["bold"]) + "  Instructions 📜",
    " " * 11 + "🏆  " + colored("[L]", "light_blue", attrs=["bold"]) + "  Leaderboards 🏆",
    " " * 11 + "🧙  " + colored("[P]", "light_blue", attrs=["bold"]) + "  Profile      🧙",
    " " * 11 + "🛒  " + colored("[M]", "light_blue", attrs=["bold"]) + "  Magic Shop   🛒",
    " " * 11 + "🚪  " + colored("[E]", "light_blue", attrs=["bold"]) + "  Exit Game    🚪"
    ]

    for option in menu_options:
        print(option.center(75))

    display_footer("Please enter a choice and press Enter.")


def display_instructions():
    '''
    Displays the game instructions and rules to the player.

    This function shows a formatted display of how to play the game,
    including game rules and available power-ups/hints. 
    '''

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

if __name__ == '__main__':
    display_main_menu()