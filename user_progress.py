import os, json, time
from termcolor import cprint, colored
from display_manager import display_body, display_border, clear_screen, welcome_display
from word_utils import get_player_input

'''
User Progress
- This module handles user profile management by interfacing with a JSON file 
('user_progress.json') to persist user data across sessions. It also handles
login/logout, stat tracking, hint purchases, and score updates for the game. 
Additionally, it supports user authentication by nickname, magic point tracking, 
hint limitations, and personal best score recording.
'''

current_user = None

MAX_PURCHASED_HINTS = 10

def load_users():
    if os.path.exists("user_progress.json"):
        try:
            with open("user_progress.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            cprint("Warning: User data file is corrupted. Starting with empty database.", "light_red")
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

    # lagyan ng better 
    if nickname not in users:
        users[nickname] = {
            "points": 0,
            "hints_purchased": [],
            "hints_available": 0,
            "highest_score": 0
        }
        save_users(users)
        clear_screen()
        welcome_display(f"Welcome, {nickname}! New wizard profile created.", nickname, 'on_white')
    else:
        clear_screen()
        welcome_display(f"Welcome back, {nickname}! Your magical journey continues...", nickname, 'on_white')
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
    Add session score to total points and update highest_score if this session was the user's best game.
    """
    global current_user
    if not current_user:
        return False
    
    users = load_users()
    user = users[current_user]
    
    # Update total magic points
    user['points'] = user.get('points', 0) + session_score

    # Update highest_score if this session is their best
    if session_score > user.get('highest_score', 0):
        user['highest_score'] = session_score

    save_users(users)
    return True



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
        cprint(f"Maximum of {MAX_PURCHASED_HINTS} whispers reached!", 'light_yellow')
        return False
    
    #Check if enough points
    if user["points"] < cost:
        print('')
        cprint(f"🚫 Not enough magic points! You have {user['points']} but a whisper costs {cost}.", "light_red", attrs=["bold"])
        return False
    
    #Deduct cost and give hint
    user["points"] -= cost
    user["hints_purchased"].append(hint_id)
    user["hints_available"] += 1
    save_users(users)
    print('')
    cprint(f"✨ Whisper attained! You have {user['points']} magic points remaining.", 'light_green', attrs=['bold'])
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
        cprint("No wizard is currently logged in!", "light_red")
        return
        
    stats = get_user_stats()
    
    profile_lines = [
        "",
        colored(f"🧙 {stats['nickname']}'s Wizard Profile 🧙", attrs=["bold"]),
        "",
        '═'*75,
        "",
        colored(f"✨ Magic Points: {stats['points']}", "white"),
        colored(f"🔮 Available Whispers: {stats['hints_available']}"),
        colored(f"🏆 Highest Score: {stats['highest_score']}"),
        "",
        '─'*75,
        "",
        colored("Press Enter to return to the main menu", attrs=["bold"]),
        ""
    ]
    
    clear_screen()
    display_border("on_light_blue")
    display_body(profile_lines, "white", "on_light_blue")
    display_border("on_light_blue")
    print("")
    input()


def display_shop():
    """
    Displays one of the main options in the main menu [M]
    
    Shows the Mystic Market:
        - Purchaseable hint for 10 Magic Points
    """

    global current_user
    
    if not current_user:
        cprint("Please log in to access the shop!", "light_red")
        return
        
    stats = get_user_stats()
    
    shop_lines = [
        "",
        colored("🛒 The Mystic Market 🛒", attrs=["bold"]),
        "",
        colored('═'*75),
        "",
        colored(f"💰 Your Magic Points 💰: {stats['points']}"),
        "",
        colored('─'*75),
        ""
    ]
    
    shop_items = [
        {"id": "basic_hint", "name": "Whisper of Guidance", "cost": 10, "description": "🔍 Reveals one letter in a hidden word"},
    ]
    
    for i, item in enumerate(shop_items, 1):
        shop_lines.append(colored(f"{i}. {item['name']} - {item['cost']} points", "white"))
        shop_lines.append(colored(f"{item['description']}", "white"))
        shop_lines.append("")
    
    shop_lines.extend([
    '-'*75,
    "",
    colored("Enter ", attrs=["bold"]) + colored("item number", "light_magenta") + \
        colored(" to purchase | [", attrs=["bold"]) + colored("e", "light_red") + colored("|", attrs=["bold"]) + \
            colored("exit", "light_red") + colored("] to exit", attrs=["bold"]),
    ""
])


    while True:
        clear_screen()
        shop_lines[5] = colored(f"💰 Your Magic Points 💰: {get_user_stats()['points']}", "white")
        
        display_border("on_magenta")
        display_body(shop_lines, "white", "on_magenta")
        display_border("on_magenta")
        print('')
        
        choice = get_player_input()
        if choice.lower() in ['e', 'exit']:
            return
            
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(shop_items):
                item = shop_items[choice_num - 1]
                if purchase_hint(item["id"], item["cost"]):
                    cprint(f"You purchased {item['name']}!", 'light_green', attrs=['bold'])
                    time.sleep(0.75)
                else:
                    time.sleep(0.75)
            else:
                raise ValueError()

        except ValueError:
            clear_screen()
            display_border("on_light_red")
            display_body(shop_lines, "white", "on_light_red")
            display_border("on_light_red")
            print('')
            cprint('Invalid Choice', "light_red", attrs=["bold"])
            time.sleep(0.75)
            continue

def use_hint():
    """
    Use one of the purchased hints.
    Returns True if a hint was successfully used, False otherwise.
    """
    global current_user
    if not current_user:
        return False
    
    users = load_users()
    user = users[current_user]
    
    if user.get("hints_available", 0) > 0:
        user["hints_available"] -= 1
        save_users(users)
        return True
    return False
