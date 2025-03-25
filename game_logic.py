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
        for idx, coordinate in enumerate(self.word):
            x, y = coordinate[idx]
            self.grid[x][y] = self.word[idx]
            

# grid = [
#     ["-", "-", "-", "x", "-"],
#     ["-", "-", "-", "x", "-"],
#     ["-", "x", "x", "x", "x"],
#     ["-", "x", "-", "-", "-"],
#     ["-", "x", "-", "-", "-"],
#     ["x", "x", "x", "x", "-"],
#     ["x", "-", "-", "-", "-"],
#     ["x", "-", "-", "-", "-"],
#     ["x", "-", "-", "-", "-"]
# ]
# positions = {
#     "TEAM": [(2, 1), (2, 2), (2, 3), (2, 4)],
#     "MEAT": [(5, 0), (5, 1), (5, 2), (5, 3)],
#     "MATE": [(5, 0), (6, 0), (7, 0), (8, 0)],
#     "TEA": [(0, 3), (1, 3), (2, 3)],
#     "TAME": [(2, 1), (3, 1), (4, 1), (5, 1)]
# }

class WordscapesGame:
    def __init__(self, letters, words, grids, positions):
        self.letters = letters
        self.words = words
        self.grids = grids
        self.positions = positions
    
    def play(self):
        pass

game = WordscapesGame(letters, words, grid, positions)
game.play()
