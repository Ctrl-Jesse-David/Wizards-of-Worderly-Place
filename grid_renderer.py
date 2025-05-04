from display_manager import title_color_changer, clear_screen, display_border, display_body, display_top
from termcolor import colored


"""
 GRID RENDERER
 
 ADD LATER-------------
 """
 

class GameGrid:
    '''
    Manages the game grid:
        incomplete_grid (list of list of str): The grid shown to the player during the game.
        complete_grid (list of list of str): The full solution grid containing all correct words.
        positions (dict): Maps each word to a list of its (row, col) positions in the grid.
    '''
    def __init__(self, incomplete_grid, complete_grid, positions):
        '''
        Initializes the GameGrid with an incomplete and complete grid, and word positions.
        '''
        self.incomplete_grid = incomplete_grid
        self.complete_grid = complete_grid
        self.positions = positions
                         
    def display_grid(self, nickname, color="white", on_color="on_white"):
        '''
        Displays the current state of the game grid to the player.
        '''
        clear_screen()
        nickname = title_color_changer(nickname)
        grid_top = display_top(f"🧙 {colored('Welcome to Wizards of Worderly Place!', attrs=['bold'])}, {nickname} 🧙")
        grid_top.append("="*75)
        display_border(on_color)
        display_body(grid_top, color, on_color)
        joined_grid = []
        for row in self.incomplete_grid:
            joined_grid.append('  '.join(row))
        display_body(joined_grid, color, on_color)

    def update_grid(self, word):
        '''
        Reveals a guessed word on the incomplete grid if it was placed correctly.
        '''
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                if (self.positions[word] == [(2 + i*2, 7 + i*2) for i in range(6)]) or ((row, col) in [(2 + i*2, 7 + i*2) for i in range(6)]):
                    self.incomplete_grid[row][col] = colored(word[idx], 'light_blue', attrs=["bold"])
                else:
                    self.incomplete_grid[row][col] = colored(word[idx], 'light_green', attrs=["bold"])
            return True
        return False

    def display_complete_grid(self, nickname, color="white", on_color="on_white"):
        '''
        Displays the full solution grid at the end of the game.
        '''
        clear_screen()
        nickname = title_color_changer(nickname)
        grid_top = display_top(f"🧙 {colored('Welcome to Wizards of Worderly Place!', attrs=['bold'])}, {nickname} 🧙")
        grid_top.append("="*75)
        display_border(on_color)
        display_body(grid_top, color, on_color)
        joined_grid = self.grid_color_changer('white')
        display_body(joined_grid, color, on_color)
    
    def grid_color_changer(self, color):
        '''
        Colors the letters of the complete grid for display.
        '''
        joined_grid = []
        for row in self.complete_grid:
            line = [colored(i, color, attrs=["bold"]) if i.isalpha() else i for i in row]
            joined_grid.append('  '.join(line))
        return joined_grid
