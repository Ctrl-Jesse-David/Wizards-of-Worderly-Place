from utilities import is_valid, GameGrid, update_leaderboard, clear_screen, display_header
import pytest
import os
import tempfile
import builtins

def test_is_valid():
    '''
    Tests the word validation function that checks if a word can be formed from given letters.
    '''
    #Test valid word
    assert is_valid("CAT", "CAT") == True
    assert is_valid("CAT", "ACT") == True
    assert is_valid("CAT", "CATT") == True
    
    #Test invalid word
    assert is_valid("DOG", "CAT") == False
    assert is_valid("CAT", "CA") == False
    
    #Test case sensitivity
    assert is_valid("cat", "CAT") == True
    assert is_valid("CAT", "cat") == True
    
    #Test repeated letters
    assert is_valid("BOOK", "BOOKK") == True
    assert is_valid("BOOKK", "BOOK") == False

def test_game_grid_initialization():
    '''
    Tests the creation of a new game grid
    '''
    grid = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    positions = {"CAT": [(0,0), (0,1), (0,2)]}
    game_grid = GameGrid(grid, positions)
    
    assert game_grid.grid == grid
    assert game_grid.positions == positions

def test_game_grid_update():
    '''
    Tests updating the game grid when a word is found
    '''
    grid = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    positions = {"CAT": [(0,0), (0,1), (0,2)]}
    game_grid = GameGrid(grid, positions)
    
    #Test successful update
    assert game_grid.update_grid("CAT") == True
    assert game_grid.grid[0] == ['C', 'A', 'T']
    
    #Test failed update
    assert game_grid.update_grid("DOG") == False
    assert game_grid.grid[0] == ['C', 'A', 'T']  # Grid should remain unchanged

def create_temp_leaderboard():
    '''
    Creates temporary leaderboard file for test
    '''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Player1: 100\n")
        f.write("Player2: 200\n")
        f.write("Player3: 150\n")
        return f.name
from utilities import update_leaderboard
from unittest.mock import patch
import builtins
import os

def test_update_leaderboard():
    temp_path = create_temp_leaderboard()

    real_open = builtins.open  # Save the real open BEFORE patching

    def mocked_open(file, mode='r', *args, **kwargs):
        if file == "leaderboard.txt":
            return real_open(temp_path, mode, *args, **kwargs)
        return real_open(file, mode, *args, **kwargs)

    try:
        with patch("builtins.open", new=mocked_open):
            update_leaderboard("Test Player", 100)

        with open(temp_path, "r") as f:
            lines = f.readlines()
            assert "Test Player: 100" in [line.strip() for line in lines]
    finally:
        os.unlink(temp_path)



def test_clear_screen():
    '''
    Tests the screen clearing function
    '''
    #Simulate system command
    def mock_system(cmd):
        return 0
    
    #Replace the real system command with sim
    import utilities
    original_system = utilities.os.system
    utilities.os.system = mock_system
    
    try:
        clear_screen()
    except Exception as e:
        utilities.os.system = original_system
        raise e
    else:
        utilities.os.system = original_system

def test_display_header():
    '''
    Tests the header display function
    '''
    #Sim screen clearing
    def mock_clear_screen():
        return 0
    
    #Replace the real clear_screen with sim
    import utilities
    original_clear_screen = utilities.clear_screen
    utilities.clear_screen = mock_clear_screen
    
    try:
        import sys
        from io import StringIO
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        #Test header display
        display_header("Test Title", "red")
        output = sys.stdout.getvalue()
        
        assert "=" * 75 in output
        assert "Test Title" in output
        assert "=" * 75 in output
        
    except Exception as e:
        sys.stdout = original_stdout
        utilities.clear_screen = original_clear_screen
        raise e
    else:
        sys.stdout = original_stdout
        utilities.clear_screen = original_clear_screen 