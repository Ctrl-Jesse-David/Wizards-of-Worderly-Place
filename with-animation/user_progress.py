import os
import json
from display_manager import display_header
from termcolor import cprint, colored

current_user = None

#Max Possible of Hints that can be bought
MAX_PURCHASED_HINTS = 10

def load_users():
    if os.path.exists("user_progress.json"):
        try:
            with open("user_progress.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            cprint("Warning: User data file is corrupted. Starting with empty database.", "red")
            return {}
    else:
        return {}
 

def save_users(users):
    with open("user_progress.json", "w") as file:
        json.dump(users, file, indent=4)

def login_user(nickname):
    """
    Log in using existing nickname or create new profile
    """
    global current_user
    users = load_users()
    
    if nickname not in users:
        users[nickname] = {
            "points": 0,
            "hints_purchased": [],
            "hints_available": 0,
            "highest_score": 0
        }
        save_users(users)
        cprint(f"Welcome, {nickname}! New wizard profile created.", "cyan")
    else:
        cprint(f"Welcome back, {nickname}! Your magical journey continues...", "cyan")
        
    current_user = nickname
    return True


def get_user_stats():
    global current_user
    if not current_user:
        return None
    
    users = load_users()
    user_data = users[current_user]
    
    return {
        "nickname": current_user,
        "points": user_data.get("points", 0),
        "hints_available": user_data.get("hints_available", 0),
        "hints_purchased": user_data.get("hints_purchased", []),
        "highest_score": user_data.get("highest_score", 0)
    }


def update_score(session_score):
    """
    Add session score to total points and update highest_score if the new total exceeds the previous high.
    """
    global current_user
    if not current_user:
        return False
    
    users = load_users()
    user = users[current_user]
    
    #Update total magic points
    total = user.get('points', 0) + session_score
    user['points'] = total

    #Update highest score to reflect peak total points
    if total > user.get('highest_score', 0):
        user['highest_score'] = total
        update_leaderboard(current_user, total)

    save_users(users)
    return True


def update_leaderboard(nickname, score):
    scores = []
    
    try:
        with open("leaderboard.txt", "r") as file:
            scores = [line.strip().split(": ") for line in file]
    except FileNotFoundError:
        pass
    
    #Check if user already exists in leaderboard
    user_exists = False
    for i, (name, old_score) in enumerate(scores):
        if name == nickname:
            user_exists = True
            if int(score) > int(old_score):
                scores[i][1] = str(score)
            break
    
    #Add new user if not found
    if not user_exists:
        scores.append([nickname, str(score)])
    
    #Write updated scores
    with open("leaderboard.txt", "w") as file:
        for name, sc in scores:
            file.write(f"{name}: {sc}\n")


def purchase_hint(hint_id, cost):
    """
    Purchase a hint (up to 10) by spending points.
    """
    global current_user
    if not current_user:
        return False
    
    users = load_users()
    user = users[current_user]

    user.setdefault("points", 0)
    user.setdefault("hints_purchased", [])
    user.setdefault("hints_available", 0)
        
    #Check purchase limit
    if user["hints_available"] >= MAX_PURCHASED_HINTS:
        cprint(f"Maximum of {MAX_PURCHASED_HINTS} hints reached!", "yellow")
        return False
    
    #Check if enough points
    if user["points"] < cost:
        cprint(f"Not enough magic points! You have {user['points']} but the hint costs {cost}.", "red")
        return False
    
    #Deduct cost and give hint
    user["points"] -= cost
    user["hints_purchased"].append(hint_id)
    user["hints_available"] += 1
    save_users(users)
    cprint(f"✨ Hint purchased! You have {user['points']} magic points remaining.", "green")
    return True

def logout_user():
    global current_user
    if current_user:
        current_user = None
        return True
    return False


def display_user_profile():
    global current_user
    
    if not current_user:
        cprint("No wizard is currently logged in!", "red")
        return
        
    stats = get_user_stats()
    
    display_header(
        title=f"🧙 {stats['nickname']}'s Wizard Profile 🧙",
        color="cyan"
    )
    
    print(f"✨ Magic Points: {stats['points']}")
    print(f"🔮 Available Hints: {stats['hints_available']}")
    print(f"🏆 Highest Score: {stats['highest_score']}")
    print("-"*75)
    
    input(colored("Press Enter to return to the main menu.", "cyan", attrs=["bold"]))


def display_shop():
    global current_user
    
    if not current_user:
        cprint("Please log in to access the shop!", "red")
        return
        
    stats = get_user_stats()
    
    display_header(
        title="✨ MAGICAL SHOP ✨",
        color="light_magenta"
    )
    
    print(f"Your Magic Points: {stats['points']}")
    print("-"*75)
    
    shop_items = [
        {"id": "basic_hint", "name": "Basic Hint", "cost": 10, "description": "Reveals one letter in a hidden word"},
        {"id": "advanced_hint", "name": "Advanced Hint", "cost": 25, "description": "Reveals a full hidden word"},
    ]
    
    for i, item in enumerate(shop_items, 1):
        print(f"{i}. {item['name']} - {item['cost']} points")
        print(f"   {item['description']}")
        print()
    
    print("-"*75)
    
    choice = input(colored("Enter item number to purchase | [e|exit] to exit: ", "light_magenta"))
    
    if choice.lower() in ['e', 'exit']:
        return
        
    try:
        item_index = int(choice) - 1
        if 0 <= item_index < len(shop_items):
            item = shop_items[item_index]
            if purchase_hint(item["id"], item["cost"]):
                cprint(f"You purchased {item['name']}!", "green")
        else:
            cprint("Invalid item number!", "red")
    except ValueError:
        cprint("Please enter a valid number.", "red")
    
    input(colored("Press Enter to continue...", "light_magenta", attrs=["bold"]))
