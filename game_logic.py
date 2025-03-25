import os
from game_levels import letters, words, grid, positions

class GameGrid:
    def __init__(self, grid, positions):
        self.grid = grid
        self.positons = positions

    def refresh_display(self):
        return os.system('cls' if os.name == 'nt' else 'clear')
                         
    def display_grid(self, grid):
        print('WELCOME TO WORDSCAPES')
        for row in self.grid:
            print(''.join(row))
        print('\n')

    def update_grid(self, word):
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                self.grid[row][col] = word[idx]
            return True
        return False



class WordscapesGame:
    def __init__(self, letters, words, grids, positions):
        self.letters = letters
        self.words = words
        self.grids = grids
        self.positions = positions
    
    def shuffle_letters(self):
        pass

    def 

    def play(self):
        pass

game = WordscapesGame(letters, words, grid, positions)
game.play()
