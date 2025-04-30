from display_manager import display_header, clear_screen, display_border, display_body, display_top

class GameGrid:
    def __init__(self, incomplete_grid, complete_grid, positions):
        self.incomplete_grid = incomplete_grid
        self.complete_grid = complete_grid
        self.positions = positions
                         
    def display_grid(self, nickname, color="white", on_color="on_white"):
        clear_screen()
    
        grid_top = display_top(f"🧙 Welcome to Wizards of Worderly Place!, {nickname} 🧙")
        grid_top.append("="*75)
        display_border(on_color)
        display_body(grid_top, color, on_color)
        joined_grid = []
        for row in self.incomplete_grid:
            joined_grid.append('  '.join(row))
        display_body(joined_grid, color, on_color)

    def display_complete_grid(self, nickname, color="white", on_color="on_white"):
        clear_screen()
    
        grid_top = display_top(f"🧙 Welcome to Wizards of Worderly Place!, {nickname} 🧙")
        grid_top.append("="*75)
        display_border(on_color)
        display_body(grid_top, color, on_color)
        joined_grid = []
        for row in self.complete_grid:
            joined_grid.append('  '.join(row))
        display_body(joined_grid, color, on_color)

    def update_grid(self, word):
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                self.incomplete_grid[row][col] = word[idx]
            return True
        return False