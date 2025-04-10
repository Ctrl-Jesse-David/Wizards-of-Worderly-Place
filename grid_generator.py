import random
from utilities import is_valid

def get_main_and_valid_words(file_path):
    def read_words():
        try:
            with open(file_path) as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            return None
    
    words = read_words()
    six_letter_words = [word for word in words if len(word) == 6]
    if not six_letter_words:
        return None
    
    main_word = random.choice(six_letter_words)
    valid_words = [word for word in words 
                  if 3 <= len(word) <= 6 
                  and is_valid(word, main_word) 
                  and word != main_word]
    
    return (main_word, valid_words) if len(valid_words) >= 20 else get_main_and_valid_words(file_path)

def place_main_diagonal(word, grid):
    for i, letter in enumerate(word.upper()):
        grid[2 + i*2][7 + i*2] = letter
    return grid

def find_intersections(word, grid):
    intersections = []
    for i, letter in enumerate(word):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == letter:
                    if (col - i >= 0 and col + len(word) - i <= len(grid[0])):
                        if all(grid[row][col-i+j] in ('.', word[j]) for j in range(len(word))):
                            intersections.append((row, col-i, 'h'))
                    if (row - i >= 0 and row + len(word) - i <= len(grid)):
                        if all(grid[row-i+j][col] in ('.', word[j]) for j in range(len(word))):
                            intersections.append((row-i, col, 'v'))
    return intersections

def is_valid_placement(word, row, col, direction, grid):
    if direction == 'h':
        for i in range(len(word)):
            cell = grid[row][col+i]
            if cell != '.' and cell != word[i]:
                return False
            if (i == 0 and col > 0 and grid[row][col-1] != '.') or \
               (i == len(word)-1 and col+i+1 < len(grid[0]) and grid[row][col+i+1] != '.'):
                return False
            if grid[row][col+i] == '.':
                if (row > 0 and grid[row-1][col+i] != '.') or (row < len(grid)-1 and grid[row+1][col+i] != '.'):
                    return False
    else: 
        for i in range(len(word)):
            cell = grid[row+i][col]
            if cell != '.' and cell != word[i]:
                return False
            if (i == 0 and row > 0 and grid[row-1][col] != '.') or \
               (i == len(word)-1 and row+i+1 < len(grid) and grid[row+i+1][col] != '.'):
                return False
            if grid[row+i][col] == '.':
                if (col > 0 and grid[row+i][col-1] != '.') or (col < len(grid[0])-1 and grid[row+i][col+1] != '.'):
                    return False
    return True

def place_word(word, grid):
    intersections = find_intersections(word, grid)
    random.shuffle(intersections)
    
    for row, col, direction in intersections:
        if is_valid_placement(word, row, col, direction, grid):
            for i, letter in enumerate(word):
                grid[row + (i if direction == 'v' else 0)][col + (i if direction == 'h' else 0)] = letter
            return True, (row, col, direction)
    
    for _ in range(100):
        direction = random.choice(['h', 'v'])
        max_row = len(grid) - (len(word) if direction == 'v' else 0)
        max_col = len(grid[0]) - (len(word) if direction == 'h' else 0)
        row, col = random.randint(0, max_row-1), random.randint(0, max_col-1)

        if is_valid_placement(word, row, col, direction, grid):
            place_word_on_grid(word, row, col, direction, grid)
            return True, (row, col, direction)
        else:
            return False, None
        
    
    return False, None

def place_word_on_grid(word, row, col, direction, grid):
    for i, letter in enumerate(word):
        if direction == 'h':
            grid[row][col + i] = letter
        else: 
            grid[row + i][col] = letter


def generate_word_grid():
    main_word, valid_words = get_main_and_valid_words("word_dictionary.txt")

    while True:
        grid = [['.' for _ in range(25)] for _ in range(15)]
        placed_words = [(main_word.upper(), (2, 7), 'd')]
        non_placed_words = []
        place_main_diagonal(main_word, grid)

        placed_count = 0
        for word in sorted(valid_words, key=len, reverse=True):
            word = word.upper()
            success, placement = place_word(word, grid)
            if success:
                placed_words.append((word, (placement[0], placement[1]), placement[2]))
                placed_count += 1
            else:
                non_placed_words.append(word.upper())

        if placed_count >= 20:
            return grid, placed_words, non_placed_words


### 
# FOR HIDING THE WORDS 
def generate_positions_dict(placed_words):
    positions = {}
    for word, coords, direction in placed_words:
        if coords == (2,7):
            r, c = coords
            positions[word] = [(r+(i*2), c+(i*2)) for i in range(6)]

        elif direction == 'h':
            row, col = coords
            positions[word] = [(row, col + i) for i in range(len(word))]

        elif direction == 'v':
            row, col = coords
            positions[word] = [(row + i, col) for i in range(len(word))]
    
    return positions

def convert_grid_to_display(grid):
    display_grid = []
    
    for row in grid:
        display_row = []
        for cell in row:
            if cell == '.':
                display_row.append('.')
            else:
                display_row.append('#')
        display_grid.append(display_row)
        
    return display_grid

def reveal_word(display_grid, word, positions):
    if word in positions:
        for i, (row, col) in enumerate(positions[word]):
            display_grid[row][col] = word[i]
    return display_grid

####

if __name__ == '__main__':
    '''para mas readable return values'''
    grid, placed_words = generate_word_grid()

    print("\nGrid:")
    for row in grid:
        print('  '.join(row))

    print("\nPlaced Words (Total: {}):".format(len(placed_words)))
    for word, coords, direction in placed_words:
        print(f"{word}: {'diagonal' if direction == 'diagonal' else f'{direction} at {coords}'}")   
