from game_logic import WordscapesGame
import pytest

def create_sample_game():
    '''
    Creates sample game instance for testing
    '''
    letters = ['C', 'A', 'T', 'D', 'O', 'G']
    incomplete_grid = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    positions = {"CAT": [(0,0), (0,1), (0,2)], "DOG": [(1,0), (1,1), (1,2)]}
    non_placed_words = ["ACT", "TAG"]
    return WordscapesGame(letters, incomplete_grid, positions, non_placed_words)

def test_game_initialization():
    '''
    Tests game initialization
    '''
    game = create_sample_game()
    
    # Check initial letters
    assert game.letters == ['C', 'A', 'T', 'D', 'O', 'G']
    assert game.words == {"CAT", "DOG"}
    
    # Check initial game state
    assert game.lives == 5
    assert game.points == 0
    assert game.found_words == set()
    assert game.hints_remaining == 3

def test_shuffle_letters():
    '''
    Tests the letter shuffling functionality
    '''
    game = create_sample_game()
    original_letters = game.letters.copy()
    
    #Shuffle
    game.shuffle_letters()
    
    #If shuffled still contains the letters
    assert set(game.letters) == set(original_letters)  #Same letters
    assert game.letters != original_letters  #Different order

def test_calculate_points():
    '''
    Tests point calculations
    '''
    game = create_sample_game()
    
    #Test for different word lengths
    assert game.calculate_points("CAT", set()) == 3
    assert game.calculate_points("DOG", set()) == 3
    
    #Test no points for already found word
    assert game.calculate_points("CAT", {"CAT"}) == 0

def test_the_guess():
    '''
    Tests the word guessing functionality
    '''
    game = create_sample_game()
    
    #Valid word guess
    game.the_guess("CAT")
    assert "CAT" in game.found_words
    assert game.points > 0
    
    #Invalid guess
    initial_lives = game.lives
    game.the_guess("XYZ")
    assert game.lives == initial_lives - 1
    
    #Already found guess
    game.the_guess("CAT")
    assert game.lives == initial_lives - 1  

def test_get_hint():
    '''
    Tests hint system
    '''
    game = create_sample_game()
    
    #Getting hint
    initial_hints = game.hints_remaining
    game.get_hint()
    assert game.hints_remaining == initial_hints - 1
    
    #Used all hints
    while game.hints_remaining > 0:
        game.get_hint()
    
    #Test no hints when none remaining
    assert game.hints_remaining == 0
    game.get_hint()