from worderly import get_player_nickname, display_menu

def test_get_player_nickname_valid_input(monkeypatch):
    #Simulates user input
    monkeypatch.setattr('builtins.input', lambda _: "TestPlayer")
    assert get_player_nickname() == "TestPlayer"

def test_get_player_nickname_empty_input(monkeypatch):
    #Simulate empty input followed by valid input
    inputs = ["", "TestPlayer"]
    input_iter = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iter))
    assert get_player_nickname() == "TestPlayer" 