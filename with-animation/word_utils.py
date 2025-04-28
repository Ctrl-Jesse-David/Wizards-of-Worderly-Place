



def is_valid(guess, letters):
    guess_cap = guess.upper()
    letters_cap = letters.upper()
    return all(guess_cap.count(letter) <= letters_cap.count(letter) 
        for letter in guess_cap)