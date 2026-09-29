# Libraries **********************************************************************

import random
import datetime

# File I/O Functions **********************************************************************

def load_Words(): # retrieve category, difficulty and word
    words = []
    try:
        fileObj = open("Words.txt", "r") # [category, diff, word]
        for line in fileObj:
            line = line.strip()
            if line != "":
                parts = line.split(",")
                if len(parts) == 3:
                    words.append([parts[0], parts[1], parts[2]])
        fileObj.close()
    except FileNotFoundError:
        print("Words.txt not found.")
    return words


def load_Categories(): # retrieve category list
    categories = []
    try:
        fileObj = open("Categories.txt", "r")
        for line in fileObj:
            line = line.strip()
            if line != "":
                categories.append(line)
        fileObj.close()
    except FileNotFoundError:
        print("Categories.txt not found.")
    return categories


def load_Scoreboard(): # retrieve initials, score and date
    scores = []
    try:
        fileObj = open("Scoreboard.txt", "r")
        for line in fileObj:
            line = line.strip()
            if line != "":
                parts = line.split(",")
                if len(parts) == 3:
                    scores.append([parts[0], int(parts[1]), parts[2]])
        fileObj.close()
    except FileNotFoundError:
        print("Scoreboard.txt not found.")
    return scores


def save_Words(words):
    fileObj = open("Words.txt", "w")
    for row in words:
        fileObj.write(row[0] + "," + row[1] + "," + row[2] + "\n")
    fileObj.close()


def save_Categories(categories):
    fileObj = open("Categories.txt", "w")
    for cat in categories:
        fileObj.write(cat + "\n")
    fileObj.close()


def save_Scoreboard(scores):
    fileObj = open("Scoreboard.txt", "w") # [initials, score, date/time]
    for row in scores:
        fileObj.write(row[0] + "," + str(row[1]) + "," + row[2] + "\n") # Score needs be converted back to string [1]
    fileObj.close()


# Snowman Function

def show_SnowMan(lives):
    stages = [
        # Melted lives = 0 (loss)
        """ 
        ( X _ X )
    
        """,
        # Lives = 1
        """
        ( *_* )
          ( )
        """,
        """
        ( *_* )
         /(:)|
        """,
        # Lives = 2
        """
        ( *_* )
         /(:)|
          (:)
        """,
        # Lives = 3
        """
        ( *_* )
         /(:)|
          (:)
          | |
        """,
        # Lives = 4
        """
        ( *_* )
        /( : )|
         ( : )
          | |
        """,
        # Lives = 5
        """
       (  *_*  )
       /(  :  )|
        (  :  )
          | |
        """
    ]

    if lives < 0:
        lives = 0
    if lives > 5:
        lives = 5
    print(stages[lives])


# Menu Functions ***********************************************************************

def main_Menu():
    print("\n*** Snowman ***")
    print("--- Main Menu -----")
    print("\t1. Play Game")
    print("\t2. Show Scoreboard")
    print("\t3. Manage Game")
    print("\t4. Save and Exit")
    try:
        print("-------------------")
        return int(input("Enter choice: "))
    except ValueError:
        return 0


def manage_Menu():
    print("\n--- Manage Game ---")
    print("\t1. Add Word")
    print("\t2. Remove Word")
    print("\t3. Add Category")
    print("\t4. Return")
    try:
        print("-------------------")
        return int(input("Enter choice: "))
    except ValueError:
        return 0



# Game management Functions ***********************************************************************************

def add_word(words, categories): # User can enter new word, its category and difficulty
    word = input("\nEnter word: ").strip()
    if word == "" or not word.isalpha(): # Makes sure not blank and is letter only
        print("Invalid input. Please enter a word made up of letters only.")
        return # bring back menu

    category = input("Assign category: ").strip()
    if category == "" or not category.isalpha():
        print("Invalid input. Please enter a category made up of letters only.")
        return

    print("\n1. Easy")
    print("2. Medium")
    print("3. Hard")
    flag = True
    while flag:
        try:
            diff = int(input("Assign difficulty: "))
            if diff == 1:
                difficulty = "easy"
                flag = False
            elif diff == 2:
                difficulty = "medium"
                flag = False
            elif diff == 3:
                difficulty = "hard"
                flag = False
            else:
                print("Invalid difficulty selection.")
        except ValueError:
            print("Invalid difficulty selection.")


    if category not in categories:
        categories.append(category) # Adds cat if it does not already exist

    words.append([category, difficulty, word])
    print("\nWord added successfully.")

def remove_word(words):
    if len(words) == 0:
        print("No words to remove.")
        return
    print("\nWords Listed:")
    for i in range(len(words)):
        print(i + 1, ".", words[i][2], "(", words[i][0],"/" ,words[i][1], ")")  # prints words in sequence numbering them up from 1
                                                                                # Easier selection as INT value than typing string
                                                                                # shows as word ( category / difficulty )
    flag = True
    while flag:
        try:
            remove_choice = int(input("Enter choice: "))
            index = remove_choice - 1
            if 0 <= index < len(words):
                removed = words.pop(index)
                print("\nWord removed successfully: ", removed[2])
                flag = False
            else:
                print("Invalid choice. Select a numbered option")
        except ValueError:
            print("Invalid inpout, enter a displayed number.")

def add_category(categories): # Adds a new category - Categories.txt
    print("\n-- Categories --")
    for cat in categories:
        print("\t-",cat)
    cat = input("Enter new category: ").strip()
    if cat != "" and cat not in categories:
        categories.append(cat)
        print("Category added.")



# Scoreboard Functions *******************************************************

def add_score(scores, difficulty):
    if difficulty == "easy":
        points = 1
    elif difficulty == "medium":
        points = 5
    else:
        points = 10

    print("\n* ADD SCORE *")
    initials = input("Enter initials (3 letters): ").upper()
    initials = initials[:3].ljust(3, "_") # take first three characters
                                                         # Other characters up to three fill as _
    # Gets the current date and time sourced
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M") # % = placeholder for number
                                                              # strftime (string format time)
                                                              # .now() pulls data from system for time and date
    found = False # Checks for player details already stored
    for row in scores:
        if row[0] == initials:
            row[1] += points
            row[2] = date
            found = True

    if not found:
        scores.append([initials, points, date])

def show_scores(scores):
    print("\n--- SCOREBOARD ---")
    if len(scores) == 0:
        print("No scores recorded.")
        return

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True) # Reverses order in descending value
                                                                    # x = row # row 1 = score
    top_scores = sorted_scores[:5]
    for row in top_scores:
        print(row[0], "-", row[1], "points -", row[2])

# Play Game Functions ***************************************************************************

def choose_category(categories): # returns in play game
    flag = True
    while flag:
        print("\n--- Categories ---")
        for cat in range(len(categories)):
            print(f"\t {cat + 1}. {categories[cat]}") # Display cats for selection as int value
        try:
            print("-------------------")
            choice = int(input("Enter Category Number: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1] # ensures choice matches index number
            else:
                print("Invalid number entered.")
        except ValueError:
            print("Invalid input entered. Enter a number.")

def choose_difficulty(): # returns in play game
    print("\n-- Difficulties --")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("-------------------")
    flag = True
    while flag:
        try:
            diff = int(input("Choose difficulty: ")) # Figured that int selection would be more user-friendly
            if diff == 1:                            # easier to manage
                return "easy"
            elif diff == 2:
                return "medium"
            elif diff == 3:
                return "hard"
            else:
                print("Invalid difficulty selection (1-3).")
        except ValueError:
            print("Invalid difficulty entered.")

def play_Game(words, categories, scores):
    category = choose_category(categories)
    difficulty = choose_difficulty()

    possible_words = []
    for row in words:
        if row[0] == category and row[1] == difficulty:
            possible_words.append(row[2]) # adds word from Words to possible list by filter from choose diff, cats

    if len(possible_words) == 0:
        print("No words available.")
        return

    secret = random.choice(possible_words)
    masked = ["_" for _ in secret] # sets each character to "_" (e.g. cat = ___)
    guessed = []
    lives = 5

    while lives > 0 and "_" in masked:
        show_SnowMan(lives) # shows snowman display for lives
        print("-------------------------")
        print("Category:", category)
        print("Difficulty:", difficulty)
        print("-------------------------")
        print("Word:", " ".join(masked))
        print("Lives:", lives)
        print("-------------------------")

        if len(guessed) > 0:
            print("Guessed letters:", ", ".join(guessed))
        else:
            print("Guessed letters: None")

        guess = input("Guess letter: ").lower().strip()

        if guess == "" or not guess.isalpha():
            print("Enter a letter A-Z.")
            continue

        letter = guess[0]

        if letter in guessed: # checks for repeat
            print("Already guessed.")
            continue

        guessed.append(letter) # adds letter to guess list

        if letter in secret.lower():
            print("________________________")
            print("\nYou have chosen....")
            print("\twisely")
            print("________________________")

            for i in range(len(secret)): # replace _ with correct letter # index variable to count up from 0
                if secret[i].lower() == letter:
                    masked[i] = secret[i]
        else:
            print("________________________")
            print("\nYou have chosen.... ")
            print("\tpoorly")
            print("________________________")
            lives -= 1

    show_SnowMan(lives) # Character called
    if "_" not in masked:
        print("**********************************")
        print("\nYOU WIN! Word was:", secret)
        print("**********************************")

        add_score(scores, difficulty)
    else:
        print("...............................")
        print("\nYOU LOSE! Word was:", secret)
        print("...............................")

# Main Program Run ***************************************************************

def main():
    words = load_Words()
    categories = load_Categories()
    scores = load_Scoreboard()
    flag = True
    while flag:
        choice = main_Menu()
        if choice == 1:
            play_Game(words, categories, scores)
        elif choice == 2:
            show_scores(scores)
        elif choice == 3:
            manage = manage_Menu()
            if manage == 1:
                add_word(words, categories)
            elif manage == 2:
                remove_word(words)
            elif manage == 3:
                add_category(categories)
        elif choice == 4:
            save_Words(words)
            save_Categories(categories)
            save_Scoreboard(scores)
            print("Data saved.")
            print("Thank you for playing. Goodbye.")
            break
        else:
            print("Invalid choice.")
main()