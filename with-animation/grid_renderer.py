from display_manager import display_header, clear_screen

class GameGrid:
    def __init__(self, incomplete_grid, complete_grid, positions):
        self.incomplete_grid = incomplete_grid
        self.complete_grid = complete_grid
        self.positions = positions
                         
    def display_grid(self, nickname):
        clear_screen()
        display_header(
            title=f"🧙 Welcome to Wizards of Worderly Place!, {nickname} 🧙",
            color="blue")
        for row in self.incomplete_grid:
            print('  '.join(row))

    def display_complete_grid(self, nickname):
        clear_screen()
        display_header(
            title=f"🧙 Welcome to Wizards of Worderly Place!, {nickname} 🧙",
            color="blue")
        for row in self.complete_grid:
            print('  '.join(row))

    def update_grid(self, word):
        if word in self.positions:
            for idx, (row, col) in enumerate(self.positions[word]):
                self.incomplete_grid[row][col] = word[idx]
            return True
        return False