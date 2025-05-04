import pytest
import random

from grid_constructor import (
    place_main_diagonal,
    find_intersections,
    is_valid_placement,
    place_word,
    generate_positions_dict,
    generate_word_grid,
    main_has_adjacent_letter
)
from word_utils import is_valid, get_wrapped_words

'''
PYTEST worderly.py
- This module includes comprehensive pytest test suite for the word game. It us used for testing 
the core grid-building and game mechanics thoroughly, including word placement functions, intersection
logic, helper functions logic, game mechanics, and edge cases (i.e. repeated guesses, lives running out, invalid word forms, etc.)
'''

# Test data
TEST_GRID = [['.' for _ in range(25)] for _ in range(15)]
TEST_MAIN_WORD = "STREAK"
TEST_POSITIONS = {
    'STREAK': [(2 + i*2, 7 + i*2) for i in range(6)],       #Main diagonal word
    'STARE': [(4, 9), (5, 9), (6, 9), (7, 9), (8, 9)],      #Vertical word
    'TAKE': [(6, 9), (6, 10), (6, 11), (6, 12)]             #Horizontal word
}
TEST_NON_PLACED_WORDS = ['TARE', 'SEAR']
TEST_LETTERS = list(TEST_MAIN_WORD)


class MockTest_Game:
    """
    Mock simple game class for testing without other dependencies
    """
    def __init__(self, letters, grid, positions, non_placed_words, complete_grid, name):
        self.letters = letters
        self.words = set(positions.keys())
        self.positions = positions
        self.non_placed_words = non_placed_words
        self.complete_grid = complete_grid
        self.name = name
        self.found_words = set()
        self.found_non_placed_words = set()
        self.lives = int(len(self.words) * 0.4)
        self.points = 0
        self.last_guess = None
        self.free_hints = 5
        self.bought_hints = 3
        self.revealed_letters = set()
    
    def calculate_points(self, guess, found_words):
        """
        1 to 1 calculate_points to original function
        """
        return len(set(self.positions[guess]) - 
            set(coordinate for word in found_words 
                for coordinate in self.positions[word]))
    
    def the_guess(self, guess, player_name):
        """
        Simplified the_guess without other dependencies (e.g termcolor)
        """
        if is_valid(guess, ''.join(self.letters)):
            if guess not in self.found_words and guess not in self.found_non_placed_words:
                if guess in self.words:
                    self.found_words.add(guess)
                    points_earned = self.calculate_points(guess, self.found_words - {guess})
                    self.points += points_earned
                    self.last_guess = guess
                    return True
                elif guess in self.non_placed_words:
                    self.found_non_placed_words.add(guess)
                    self.lives += 1
                    self.last_guess = guess
                    return True
                else:
                    self.lives -= 1
                    return False
            else:
                return False
        else:
            self.lives -= 1
            return False

#Create game instance for testing
def create_game():
    """
    Create a test game instance
    """
    return MockTest_Game(
        TEST_LETTERS,
        TEST_GRID,
        TEST_POSITIONS,
        TEST_NON_PLACED_WORDS,
        TEST_GRID,
        "test_player"
    )

def test_place_main_diagonal():
    """
    Test placing the main diagonal word
    """
    grid = [['.' for _ in range(25)] for _ in range(15)]
    word = "STREAK"
    result = place_main_diagonal(word, grid)
    
    #The diagonal placement puts STREAK at positions:
    #S: (2,7), T: (4,9), R: (6,11), E: (8,13), A: (10,15), K: (12,17)
    
    #Check if word is placed correctly in diagonal positions
    for i, letter in enumerate(word):
        assert result[2 + i*2][7 + i*2] == letter.upper()
    
    #Check if other cells remain unchanged
    assert result[0][0] == '.'
    assert result[1][1] == '.'
    
    #Test with a different word length
    grid = [['.' for _ in range(25)] for _ in range(15)]
    word = "HELLO"
    result = place_main_diagonal(word, grid)
    for i, letter in enumerate(word):
        assert result[2 + i*2][7 + i*2] == letter.upper()

def test_find_intersections():
    """
    Test finding valid word intersections
    """
    grid = [['.' for _ in range(25)] for _ in range(15)]
    #Place main diagonal word
    place_main_diagonal("STREAK", grid)
    
    #Test finding intersections with main word
    intersections = find_intersections("STARE", grid)

    assert len(intersections) > 0
    for row, col, direction in intersections:
        assert 0 <= row < 15
        assert 0 <= col < 25
        assert direction in ['h', 'v']
    
    #Test word with no valid intersections
    intersections = find_intersections("ZZZ", grid)
    assert len(intersections) == 0
    
    #Test word with multiple intersections
    intersections = find_intersections("SET", grid)
    assert len(intersections) > 0
    
    #Test empty grid
    empty_grid = [['.' for _ in range(25)] for _ in range(15)]
    intersections = find_intersections("STARE", empty_grid)
    assert len(intersections) == 0

def test_is_valid_placement():
    """
    Test word placement validation
    """
    grid = [['.' for _ in range(25)] for _ in range(15)]
    place_main_diagonal("STREAK", grid)
    
    #Find actual valid intersections
    intersections = find_intersections("STARE", grid)
    if intersections:
        row, col, direction = intersections[0]
        assert is_valid_placement("STARE", row, col, direction, grid) == True
    
    #Test invalid placements
    assert is_valid_placement("STARE", -1, -1, 'h', grid) == False  #Out of bounds
    assert is_valid_placement("STARE", 15, 0, 'h', grid) == False   #Out of bounds row
    assert is_valid_placement("STARE", 0, 25, 'h', grid) == False   #Out of bounds column
    
    #Test placement that would extend beyond grid
    assert is_valid_placement("VERYLONGWORD", 0, 20, 'h', grid) == False
    
    #Overlapping with an existing word in a conflicting way
    assert is_valid_placement("ZZZ", 2, 7, 'h', grid) == False  #Conflicts with S in STREAK

    t_intersections = find_intersections("TAKE", grid)
    if t_intersections:
        t_row, t_col, t_dir = t_intersections[0]
        assert is_valid_placement("TAKE", t_row, t_col, t_dir, grid) == True

def test_place_word():
    """
    Test placing a word on the grid
    """
    grid = [['.' for _ in range(25)] for _ in range(15)]
    
    #For testing
    placed_word = ("STARE", (5, 5), 'h')
    
    word, (row, col), direction = placed_word
    if direction == 'h':
        for i, letter in enumerate(word):
            grid[row][col+i] = letter.upper()
    
    #Verify the word was placed correctly
    assert grid[5][5] == 'S'
    assert grid[5][6] == 'T'
    assert grid[5][7] == 'A'
    assert grid[5][8] == 'R'
    assert grid[5][9] == 'E'
    assert grid[5][10] == '.'

    #False assertion (deliberately incorrect)
    assert not grid[5][9] == 'X' #False assertion if not placed correctly
    assert not grid[5][9] == 1 #False assertion if a number was placed
    assert not grid[5][9] == '.' #False assertion if it's still a dot

def test_generate_positions_dict():
    """
    Test position dictionary generation
    """
    placed_words = [
        ("STREAK", (2, 7), 'd'),  #Main diagonal word
        ("STARE", (4, 9), 'v'),     #Vertical word
        ("TAKE", (6, 9), 'h')      #Horizontal word
    ]
    
    positions = generate_positions_dict(placed_words)
    
    #Check main diagonal word positions
    assert positions["STREAK"] == [(2 + i*2, 7 + i*2) for i in range(6)]
    
    #Check vertical word positions
    assert positions["STARE"] == [(4, 9), (5, 9), (6, 9), (7, 9), (8, 9)]
    
    #Check horizontal word positions
    assert positions["TAKE"] == [(6, 9), (6, 10), (6, 11), (6, 12)]

    #Deliberately incorrect position
    assert not(positions["STARE"] == [(4, 9), (4, 10), (4, 11), (4, 12), (4, 13)])


def test_is_valid():
    """
    Test word validation function
    """
    #Test valid words from main word letters
    assert is_valid("STREAK", "STREAK") == True
    assert is_valid("STEAK", "STREAK") == True
    assert is_valid("TEAK", "STREAK") == True
    assert is_valid("STAKE", "STREAK") == True
    
    #Test invalid words
    assert is_valid("XYZ", "STREAK") == False      #Invalid letters
    assert is_valid("STROOK", "STREAK") == False  #Letter not available
    
    #Edge cases
    assert is_valid("", "STREAK") == True          #Empty string is valid
    assert is_valid("STREAK", "") == False         #No letters available
    assert is_valid("streak", "STREAK") == True    #Case insensitive
    
    #Test with repeated letters
    assert is_valid("KEEE", "STREAK") == False     #Too many

def test_game_initialization():
    """
    Test game initialization with correct parameters
    """
    game = create_game()
    assert game.letters == TEST_LETTERS
    assert game.words == set(TEST_POSITIONS.keys())
    assert game.found_words == set()
    assert game.lives == int(len(game.words) * 0.4)
    assert game.points == 0
    assert game.free_hints == 5
    assert game.bought_hints == 3 

def test_calculate_points():
    """
    Test point calculation
    """
    game = create_game()

    points = game.calculate_points("STREAK", set())
    assert points == 6  #STREAK has 6 letters/positions

    assert not points == 5 #False assertion -> fails since incorrect handling of points
    assert not points == 'a' #False assertion -> fails if point is a str
    

    found_words = {"STREAK"}
    points = game.calculate_points("STARE", found_words)
    #STARE positions: [(4, 9), (5, 9), (6, 9), (7, 9), (8, 9)]
    #STREAK positions: [(2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17)]
    assert points == 4  #4 positions not overlapping with STREAK

    assert not points == 5 #False assertion -> fails since incorrect handling of points
    assert not points == 'z' #False assertion -> fails if point is a str
    
    #Test with two previously found words
    found_words = {"STREAK", "STARE"}
    points = game.calculate_points("TAKE", found_words)
    
    #TAKE positions: [(6, 9), (6, 10), (6, 11), (6, 12)]
    assert points == 2  #Only 2 positions not overlapping with STREAK or STARE

    assert not points == 3 #False assertion (1)
    assert not points == '-' #False assertion (2) -> fails if points is a symbol
    assert not points == 'a'  # False assertion (3) –> fails if points is alphabetic

def test_invalid_word_with_valid_letters():
    """
    Test word that uses valid letters but not in word list
    """
    game = create_game()
    initial_lives = game.lives
    
    #"RATE" uses valid letters but isn't in words list
    game.the_guess("RATE", "test_player")
    assert game.lives == initial_lives - 1
    assert "RATE" not in game.found_words
    assert "RATE" not in game.found_non_placed_words

def test_correct_word_guess():
    """
    Test correct word guessing mechanics
    """
    game = create_game()
    #Test correct word in grid
    game.the_guess("STREAK", "test_player")
    assert "STREAK" in game.found_words
    assert game.points > 0
    assert game.lives == int(len(game.words) * 0.4)  #Lives unchanged

def test_incorrect_word_guess():
    """
    Test incorrect word guessing mechanics
    """
    game = create_game()
    initial_lives = game.lives
    game.the_guess("XYZ", "test_player")
    assert game.lives == initial_lives - 1
    assert game.points == 0
    assert len(game.found_words) == 0

def test_repeated_word_guess():
    """
    Test handling of repeated word guesses
    """
    game = create_game()
    #First guess
    game.the_guess("STREAK", "test_player")
    initial_lives = game.lives
    initial_points = game.points
    
    #Try same word again
    game.the_guess("STREAK", "test_player")
    assert game.lives == initial_lives
    assert game.points == initial_points

def test_game_completion():
    """
    Test game completion conditions
    """
    game = create_game()
    # Guess all words
    for word in game.words:
        game.the_guess(word, "test_player")
    
    assert len(game.found_words) == len(game.words)
    assert game.lives > 0 

def test_game_over():
    """
    Test game over condition when lives run out
    """
    game = create_game()
    
    #Keep guessing invalid words until lives run out
    while game.lives > 0:
        game.the_guess("XYZ", "test_player")
    
    assert game.lives == 0
    assert len(game.found_words) < len(game.words)

def test_generate_word_grid():
    """
    Test the complete grid generation function
    """
    dictionary_file = "corncob-lowercase.txt" #For unit testing (Change txt file if necessary)
    
    grid, placed_words, non_placed_words = generate_word_grid(dictionary_file, 21, 25)  #Apprentice level difficulty instance
    
    #Check grid dimensions
    assert len(grid) == 15
    assert len(grid[0]) == 25

    #False assertiom
    assert not len(grid) == 16 #wrong coords
    assert not len(grid[0]) == 26 #wrong coords
    
    #Check that some words are placed
    assert len(placed_words) >= 21  #Min parameter
    assert len(placed_words) <= 25  #Max parameter
    
    #False assertion
    assert not len(placed_words) < 21  #Wrong min parameter
    assert not len(placed_words) > 25  #Wrong max parameter

    #Validate that placed_words format is correct (word, (row, col), direction)
    for word_info in placed_words:
        assert len(word_info) == 3
        assert isinstance(word_info[0], str)
        assert isinstance(word_info[1], tuple)
        assert word_info[2] in ['h', 'v', 'd']
    
    #Check that main word (first in list) is placed in diagonal
    assert placed_words[0][2] == 'd'

    #False assertion (shows that it is not h or v)
    assert not placed_words[0][2] == 'h' 
    assert not placed_words[0][2] == 'v'
    
def test_main_has_adjacent_letter():
    """
    Test for main_has_adjacent_letter
    """
    grid = [['.' for _ in range(25)] for _ in range(15)]
    
    #Main diag
    word = "STREAK"
    for i, letter in enumerate(word):
        grid[2 + i*2][7 + i*2] = letter.upper()
    
    #No adjacent letters 
    assert main_has_adjacent_letter(grid) == False

    #Add adjacent letters to all diagonal positions
    for i in range(len(word)):
        r, c = 2 + i*2, 7 + i*2
        grid[r][c + 1] = 'X'    #Adding letter to the right of each diagonal letter
    
    #All letters have adjacent letters
    assert main_has_adjacent_letter(grid) == True
    
    #Remove one adjacent letter (should be False)
    middle_idx = len(word) // 2
    r, c = 2 + middle_idx*2, 7 + middle_idx*2
    grid[r][c + 1] = '.'    #Remove the adjacent letter
    assert main_has_adjacent_letter(grid) == False