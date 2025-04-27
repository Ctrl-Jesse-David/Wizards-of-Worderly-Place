
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

    print((" "*11 + "📖  " + colored("[S]", "light_blue", attrs=["bold"]) + "  Start Game   📖").center(75))
    print((" "*11 + "📜  " + colored("[I]", "light_blue", attrs=["bold"]) + "  Instructions 📜").center(75))
    print((" "*11 + "🏆  " + colored("[L]", "light_blue", attrs=["bold"]) + "  Leaderboards 🏆").center(75))
    print((" "*11 + "🚪  " + colored("[E]", "light_blue", attrs=["bold"]) + "  Exit Game    🚪").center(75))

    print("-" * 75)
    print("Please enter a choice and press Enter.".center(75))
    print("=" * 75)