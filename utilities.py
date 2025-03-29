import os
from termcolor import cprint

def clear_screen():
    return os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title, color):
    clear_screen()
    print("="*75)
    cprint(title.center(75), color, attrs=["bold"])
    print("="*75)

def is_valid(guess, letters):
    return all(guess.count(letter) <= letters.count(letter) 
        for letter in guess)

def update_leaderboard(name, score):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name}: {score}\n")

class GameGrid:
    def __init__(self, grid, positions):
        self.grid = grid
        self.positions = positions
                         
    def display_grid(self, nickname):
        clear_screen()
        display_header(
            title=f"🧙 Welcome to Wizards of Worderly Place!, {nickname} 🧙",
            color="blue")
        for row in self.grid:
            print('  '.join(row))

    def update_grid(self, word):
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                self.grid[row][col] = word[idx]
            return True
        return False

'''
mga random functions
'''