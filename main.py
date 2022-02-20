# Importing modules
import os
import random
import time
import sys
from pypresence import Presence
from firebase_init import firebase
import getpass
from cryptography.fernet import Fernet
from sys import platform
import colorama
from colorama import Fore
client_id = "927479998510669834"  # Put your Client ID in here
RPC = Presence(client_id)  # Initialize the Presence client
RPC.connect() # Start the handshake loop
auth = firebase.auth()
db = firebase.database()
def write_key():
    """
    Generates a key and save it into a file
    """
    #check if the file exists
    if not os.path.exists("./assets/key.key"):
        #generate a key
        key = Fernet.generate_key()
        with open("./assets/key.key", "wb") as key_file:
            key_file.write(key)
    else:
        pass
def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("./assets/key.key", "rb").read()
    #close
    key_file.close()



#def fight
def fight():
    global enemy_name
    global enemy_health
    global enemy_attack
    global enemy_defense
    # var enemy names and enemy stats
    enemy_names = ["Goblin", "Orc", "Skeleton", "Zombie"]
    enemy_healths = [100, 200, 300, 400]
    enemy_attacks = [10, 20, 30, 40]
    enemy_defenses = [10, 20, 30, 40]
    # random enemy
    enemy_name = random.choice(enemy_names)
    enemy_health = int(random.choice(enemy_healths))
    enemy_attack = int(random.choice(enemy_attacks))
    enemy_defense = int(random.choice(enemy_defenses))
    def FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense):
        RPC.update(state="Figthing", details=f"Fighting {enemy_name}",large_image="erased_rpg",large_text="Erased RPG") # Updates our presence
        token = auth.current_user['localId']
        health = int(db.child("users").child(token).child("health").get().val())
        attack = int(db.child("users").child(token).child("attack").get().val())
        defense = int(db.child("users").child(token).child("defense").get().val())
        # enemy stats
        print(f"Computer: You have encountered a {enemy_name}!")
        print(f"Computer: {enemy_name} has {enemy_health} health!")
        print(f"Computer: {enemy_name} has {enemy_attack} attack!")
        print(f"Computer: {enemy_name} has {enemy_defense} defense!")
        # player stats
        print(f"Computer: You have {health} health!")
        print(f"Computer: You have {attack} attack!")
        print(f"Computer: You have {defense} defense!")
        # fight
        if int(health) < 0:
            health = 0
            db.child("users").child(token).child("health").set(health)
        while enemy_health > 0 and int(health) > 0:
            print("Computer: What would you like to do?")
            print(f"{Fore.RED}Computer: 1. Attack")
            print(f"{Fore.YELLOW}Computer: 2. Defend")
            print(f"{Fore.GREEN}Computer: 3. Heal")
            print(f"{Fore.BLUE}Computer: 4. Run{Fore.RESET}")
            answer = input("Player: ")
            if answer == "1":
                enemy_health = enemy_health - attack
                health = health - enemy_attack
                print(f"Computer: {enemy_name} has {enemy_health} health!")
                if int(health) < 0:
                    health = 0
                    db.child("users").child(token).child("health").set(health)
                print(f"Computer: You have {health} health!")
                db.child("users").child(token).child("health").set(health)
                FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense)
            elif answer == "2":
                enemy_health = enemy_health - (attack * 0.5)
                health = health - (enemy_attack * 0.5)
                print(f"Computer: {enemy_name} has {enemy_health} health!")
                if int(health) < 0:
                    health = 0
                    db.child("users").child(token).child("health").set(health)
                print(f"Computer: You have {health} health!")
                db.child("users").child(token).child("health").set(health)
                FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense)
            elif answer == "3":
                heals = db.child("users").child(token).child("inventory").child("healing_potions").get()
                if heals.val() is not None and int(heals.val()) != 0:
                    heals = int(heals.val())
                    db.child("users").child(token).child("inventory").child("healing_potions").set(heals - 1)
                    health = health + 50
                    if int(health) < 0:
                        health = 0
                        db.child("users").child(token).child("health").set(health)
                    print(f"Computer: You have {health} health!")
                    db.child("users").child(token).child("health").set(health)
                    FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense)
                else:
                    print("Computer: You don't have any healing potions!")
            elif answer == "4":
                print("Computer: You ran away!")
                game()
            else:
                print("Computer: Invalid input!")
                FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense)
        if enemy_health <= 0:
            print("Computer: You have defeated the enemy!")
            print("Computer: You have gained 10 exp!")
            exp = db.child("users").child(token).child("exp").get()
            exp = int(exp.val())
            exp = exp + 10
            db.child("users").child(token).child("exp").set(exp)
            game()
        elif health <= 0:
            print("Computer: You have been defeated!")
            game()
    FIGHTLOL(enemy_name, enemy_health, enemy_attack, enemy_defense)
        


#def play
def play():
    token = auth.current_user['localId']
    print("Computer: You are now playing!")
    print("Computer: What would you like to do?")
    print(f"{Fore.RED}Computer: 1. Fight")
    print(f"{Fore.GREEN}Computer: 2. Heal")
    print(f"{Fore.BLUE}Computer: 3. Shop")
    print(f"{Fore.MAGENTA}Computer: 4. Inventory")
    print(f"{Fore.CYAN}Computer: 5. Stats")
    print(f"{Fore.LIGHTBLUE_EX}Computer: 6. Logout")
    print(f"{Fore.LIGHTMAGENTA_EX}Computer: 7. Quit{Fore.RESET}")
    answer = input("Player: ")
    if answer == "1":
        print("Computer: You are now in the fight!")
        fight()
    elif answer == "2":
        #heal
        heals = db.child("users").child(token).child("inventory").child("healing_potions").get().val()
        if heals is not None and int(heals) != 0:
            heals = int(heals)
            db.child("users").child(token).child("inventory").child("healing_potions").set(heals - 1)
            health = db.child("users").child(token).child("health").get()
            health = int(health.val())
            health = health + 50
            db.child("users").child(token).child("health").set(health)
            print("Computer: You have been healed!")
        else:
            print("Computer: You don't have any healing potions!")
        play()
    elif answer == "3":
        #shop
        print("Computer: You are now in the shop!")
        # add healing potions into the shop
        print("Computer: What would you like to do?")
        print(f"{Fore.RED}Computer: 1. Buy healing potions")
        print(f"{Fore.GREEN}Computer: 2. Buy sword")
        print(f"{Fore.YELLOW}Computer: 3. Buy shield")
        print(f"{Fore.BLUE}Computer: 4. Buy armor")
        print(f"{Fore.MAGENTA}Computer: 5. Go back{Fore.RESET}")
        answer = input("Player: ")
        if answer == "1":
            #buy healing potions using money
            money = db.child("users").child(token).child("money").get().val()
            if money is not None and int(money) >= 50:
                money = int(money)
                money = money - 50
                db.child("users").child(token).child("money").set(money)
                heals = db.child("users").child(token).child("inventory").child("healing_potions").get().val()
                if heals is not None:
                    heals = int(heals)
                    heals = heals + 1
                    db.child("users").child(token).child("inventory").child("healing_potions").set(heals)
                    print("Computer: You have bought a healing potion!")
                    play()
                else:
                    db.child("users").child(token).child("inventory").child("healing_potions").set(1)
                    print("Computer: You have bought a healing potion!")
                    play()
            else:
                print("Computer: You don't have enough money!")
                play()
        elif answer == "2":
            #buy sword
            money = db.child("users").child(token).child("money").get().val()
            sword = db.child("users").child(token).child("inventory").child("sword").get().val()
            if sword is not None:
                #check if the money is enough
                if money is not None and int(money) >= 1000:
                    #check if the attack exeeds the max
                    attack = db.child("users").child(token).child("attack").get().val()
                    if attack is not None and int(attack) <= 9999:
                        money = int(money)
                        money = money - 1000
                        db.child("users").child(token).child("money").set(money)
                        #if you already have a sword
                        print("Increasing the damage of your sword!")
                        attack = int(attack)
                        attack = attack + 10
                        db.child("users").child(token).child("attack").set(attack)
                        print(f"Computer: The damage of your sword has increased by 10, now your attack is: {db.child('users').child(token).child('attack').get().val()}!")
                    else:
                        print("Computer: You already have the max damage!")
                else:
                    print("Computer: You don't have enough money!")
                play()
            else:    
                if money is not None and int(money) >= 500:
                    money = int(money)
                    money = money - 500
                    db.child("users").child(token).child("money").set(money)
                    db.child("users").child(token).child("inventory").child("sword").set(1)
                    #increse the attack
                    attack = db.child("users").child(token).child("attack").get().val()
                    attack = int(attack)
                    attack = attack + 10
                    db.child("users").child(token).child("attack").set(attack)
                    print("Computer: You have bought a sword!")
                    #by how much the attack increased
                    print(f"Computer: The damage of your sword has increased by 10 now your attack is: {db.child('users').child(token).child('attack').get().val()}!")
                    play()
        elif answer == "3":
            #buy shield
            money = db.child("users").child(token).child("money").get().val()
            shield = db.child("users").child(token).child("inventory").child("shield").get().val()
            if shield is not None:
                print("Computer: You already have a shield!")
            else:
                if money is not None and int(money) >= 500:
                    money = int(money)
                    money = money - 500
                    db.child("users").child(token).child("money").set(money)
                    db.child("users").child(token).child("inventory").child("shield").set(1)
                    print("Computer: You have bought a shield!")
                    #increase the defense
                    defense = db.child("users").child(token).child("defense").get().val()
                    defense = int(defense)
                    defense = defense + 5
                    db.child("users").child(token).child("defense").set(defense)
                    print(f"Computer: The defense of your shield has increased by 5 now your defense is: {db.child('users').child(token).child('defense').get().val()}!")
                    play()
                else:
                    print("Computer: You don't have enough money!")
                play()
        elif answer == "4":
            #buy armor
            money = db.child("users").child(token).child("money").get().val()
            armor = db.child("users").child(token).child("inventory").child("armor").get().val()
            if armor is not None:
                #check if the money is enough
                if money is not None and int(money) >= 1000:
                    #check if the defense exeeds the max
                    defense = db.child("users").child(token).child("defense").get().val()
                    if defense is not None and int(defense) <= 999:
                        money = int(money)
                        money = money - 1000
                        db.child("users").child(token).child("money").set(money)
                        print("Increasing the defense of your armor!")
                        defense = int(defense)
                        defense = defense + 5
                        db.child("users").child(token).child("defense").set(attack)
                        print(f"Computer: The defense of your armor has increased by 5, now your defense is: {db.child('users').child(token).child('defense').get().val()}!")
                    else:
                        print("Computer: You already have the max defense!")
                    play()
                else:
                    print("Computer: You don't have enough money!")
                play()
            else:
                if money is not None and int(money) >= 500:
                    money = int(money)
                    money = money - 500
                    db.child("users").child(token).child("money").set(money)
                    db.child("users").child(token).child("inventory").child("armor").set(1)
                    print("Computer: You have bought a armor!")
                    #increase the defense
                    defense = db.child("users").child(token).child("defense").get().val()
                    defense = int(defense)
                    defense = defense + 5
                    db.child("users").child(token).child("defense").set(defense)
                    print(f"Computer: The defense of your armor has increased by 5, now your defense is: {db.child('users').child(token).child('defense').get().val()}!")
                    play()
        elif answer == "5":
            print("Computer: Going back!")
            play()
        else:
            print("Computer: Invalid answer!")
        play()
    elif answer == "4":
        #inventory
        print("Computer: You are now in the inventory!")
        # get the invetnory from the database
        inventory = db.child("users").child(token).child("inventory").get()
        if inventory is not None:
            print("You have the following items:")
            print(f"{Fore.RED}Healing Potions: " + str(db.child("users").child(token).child("inventory").child("healing_potions").get().val()))
            print(f"{Fore.GREEN}Sword: " + str(db.child("users").child(token).child("inventory").child("sword").get().val()))
            print(f"{Fore.YELLOW}Shield: " + str(db.child("users").child(token).child("inventory").child("shield").get().val()))
            print(f"{Fore.BLUE}Armor: " + str(db.child("users").child(token).child("inventory").child("armor").get().val()))
            print(f"{Fore.CYAN}Money: " + str(db.child("users").child(token).child("money").get().val()) + Fore.RESET)
        play()
    elif answer == "5":
        health = db.child("users").child(token).child("health").get()
        attack = db.child("users").child(token).child("attack").get()
        defense = db.child("users").child(token).child("defense").get()
        money = db.child("users").child(token).child("money").get()
        level = db.child("users").child(token).child("level").get()
        exp = db.child("users").child(token).child("exp").get()
        print(f"""Computer: Your stats are:
{Fore.RED}Health: {health.val()}
{Fore.BLUE}Attack: {attack.val()}
{Fore.GREEN}Defense: {defense.val()}
{Fore.YELLOW}Money: {money.val()}
{Fore.MAGENTA}Level: {level.val()} {Fore.RESET}""")
        play()    
    elif answer == "6":
        os.remove("./assets/useremail.txt")
        os.remove("./assets/userpass.txt")
        print("Computer: You are now logged out!")
        newPlayer()
    elif answer == "7":
        print("Computer: You are now quitting!")
        quit()
    else:
        print("Computer: Invalid input!")
        play()


#def game
def game():
    RPC.update(state="Playing", details="In the menu",large_image="erased_rpg",large_text="Erased RPG") # Updates our presence
    token = auth.current_user['localId']
    print("Computer: Welcome back!")
    print("Computer: What would you like to do?")
    print(f"{Fore.GREEN}Computer: 1. Play")
    print(f"{Fore.YELLOW}Computer: 2. Logout")
    print(f"{Fore.RED}Computer: 3. Quit{Fore.RESET}")
    answer = input("Player: ")
    if answer == "1":
        play()
    elif answer == "2":
        os.remove("./assets/useremail.txt")
        os.remove("./assets/userpass.txt")
        print("Computer: You are now logged out!")
        newPlayer()
    elif answer == "3":
        print("Computer: You are now quitting!")
        quit()
    else:
        print("Computer: Invalid input!")
        game()        


# Defining variables
def newPlayer():
    RPC.update(state="New Player", details="Creating a new account or Logging into an existing account",large_image="erased_rpg",large_text="Erased RPG") # Updates our presence
    write_key()
    key = load_key()
    f = Fernet(key)
    #check if path exists called "assets/useraccount.txt" and "./assets/userpass.txt"
    if os.path.exists("./assets/useremail.txt") and os.path.exists("./assets/userpass.txt"):
        with open("./assets/useremail.txt", "rb") as email_file:
            email = f.decrypt(email_file.read())
            #close
            email_file.close()
        with open("./assets/userpass.txt", "rb") as password_file:
            password = f.decrypt(password_file.read())
            #close
            password_file.close()
        password = str(password).replace("b", '')
        password = str(password).replace("'", '')
        email = str(email).replace("b", '')
        email = str(email).replace("'", '')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Computer: You are now logged in!")
            game()
        except:
            os.remove("./assets/useremail.txt")
            os.remove("./assets/userpass.txt")
            print("Computer: An error ouccured please try again!")
            newPlayer()
        

    print("Computer: Welcome to Erased RPG!")
    print("Computer: Do you already have an account? (y/n)")
    answer = input("Player: ")
    if answer.lower() == "y" or answer.lower() == "yes":
        print("Computer: Please enter your email")
        email = input("Player: ")
        print("Computer: Please enter your password")
        password = getpass.getpass("Player: ")
        with open("./assets/useremail.txt", "wb") as email_file:
            email_file.write(f.encrypt(email.encode()))
            #close
            email_file.close()
        with open("./assets/userpass.txt", "wb") as password_file:
            password_file.write(f.encrypt(password.encode()))                    
            #close
            password_file.close()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            token = auth.current_user['localId']
            isUserInDB = db.child("users").child(token).get()
            if isUserInDB.val() == None:
                print("Computer: You are now creating a new account!")
                print("Computer: Please enter your username")
                username = input("Player: ")
                stats={
                    "username": username,
                    "health": 100,
                    "attack": 10,
                    "defense": 10,
                    "money": 500,
                    "level": 1,
                    "exp": 0
                }
                db.child("users").child(token).set(stats)
                print(f"Computer: You are now logged in as {username}.")
            os.system("clear")
            game()
        except Exception as e:
            os.remove("./assets/useremail.txt")
            os.remove("./assets/userpass.txt")
            print(e)
            print("Computer: Invalid email or password")
            newPlayer()
    elif answer.lower() == "n" or answer.lower() == "no":
        print("Computer: Please enter your email")
        email = input("Player: ")
        print("Computer: Please enter your password")
        password = getpass.getpass("Player: ")
        try:
            user = auth.create_user_with_email_and_password(email, password)
            token=auth.current_user['localId']
            isUserInDB = db.child("users").child(token).get()
            if isUserInDB.val() == None:
                print("Computer: You are now creating a new account!")
                print("Computer: Please enter your username")
                username = input("Player: ")
                stats={
                    "username": username,
                    "health": 100,
                    "attack": 10,
                    "defense": 10,
                    "money": 500,
                    "level": 1,
                    "exp": 0
                }
                db.child("users").child(token).set(stats)
                print(f"Computer: You are now logged in as {username}.")
                # write email and password to files
                with open("./assets/useremail.txt", "wb") as email_file:
                    email_file.write(f.encrypt(email.encode()))
                    #close
                    email_file.close()
                with open("./assets/userpass.txt", "wb") as password_file:
                    password_file.write(f.encrypt(password.encode()))
                    #close
                    password_file.close()
                os.system("clear")
                game()
            else:
                print("Computer: This email is already in use")
                newPlayer()
            return True
        except Exception as e:
            os.remove("./assets/useremail.txt")
            os.remove("./assets/userpass.txt")
            print(e)
            print("Computer: Something went wrong, please try again.")
            newPlayer()
    else:
        print("Computer: Invalid input")
        newPlayer()

if __name__ == '__main__':
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")
    newPlayer()