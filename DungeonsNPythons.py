# Code author: Patrick Woolard
# Email: Jwoolard@augusta.edu

'''
Welcome to Dungeons & Pythons!

To run the app, just run 'python DungeonsNPythons.py' in the shell of your choosing.

Ensure that you have support for the following modules in your python environment:

- "requests" (For Webscrapping):     pip install requests
- "bs4" (Parses Webscrapped Data):   pip install bs4
'''

# List of necessary modules used to execute Dungeons & Pythons

import shelve # storing character information so it gets saved across multiple sessions
import random # mainly used for simulating rolling dice
import webbrowser as wb # used to open up web browsers to give users more information about some part of Dungeons and Dragons
import requests # used to web scrape information off the internet to provide users with more information when designing a character
import bs4 # useful tool to help parse and format the web scrapped data
import os # use to handle file/folder control operations 
import platform # used to check operating system of user to prevent non-Windows users from crashing the app if they use 'Character Share' feature 
import socket # used to handle tcp communication for the 'Character Share' feature 
from zipfile import ZipFile # used to consolidate and extract shelve files for the 'Character Share' feature 
import shutil # only used to delete temporary directories once they are no longer needed 


class Character: # This is what gets saved in shelve
    
  # These get filled out in creation mode using constructor
  race = None
  charClass = None
  name = None
  age = None
  gender = None
  abScores = None # This one can be updated later in character management mode
  # These get filled out in creation mode using constructor


  def __init__(self, r, c, n, a, g, abS):
    self.race = r
    self.charClass = c
    self.name = n
    self.age = a
    self.gender = g
    self.abScores = abS
    self.sessGoals = []
    self.inventory = []

  # These get updated in character management mode
  level = "Not yet set... (Some campaigns require you start at higher levels)"
  gold = "0"
  alignment = "Not yet set... (your character's true nature may emerge as their adventures unfold)"
  sessGoals = None # "If you have any goals or notes for the next play session \n(i.e. 'I curently have 5 health points' or 'sell magic staff') "
  inventory = None
  backStory = "Not yet set... (Give your character a back story, it will help bring them more to life!)"

  # These get updated in character management mode



def characterManager(CharObj):
  '''
  After the character is made, the user will use this to manage said character.
  '''

  while True:

    print("\n \t\tCharacter Information" + "\n \t\t" + 21*"-")
    print(f"\n+ Race : {CharObj.race}") 
    print("+ Class: " + CharObj.charClass)
    print("+ Name: " + CharObj.name)
    print("+ Age: " + CharObj.age)
    print("+ Gender: " + CharObj.gender)
    print("+ Alignment: " + CharObj.alignment)
    print(f'+ Backstory: \n\t"{CharObj.backStory}"')
    
    print("\n \t\tCharacter Stats" + "\n \t\t" + 15*"-")
    print(f"* Level: {CharObj.level}")
    print("* Ability scores: \n\t" + str(CharObj.abScores))
    print("* Gold: " + CharObj.gold + "gp")
    print(f"* Inventory Items: \n\t{CharObj.inventory}\n")
    print(f"* Character Goals/Notes: \n\t{CharObj.sessGoals}\n")



    print(f"What would you like to do with {CharObj.name}? (Please select row number)\n")

    print("1) Update Alignment")
    print("2) Update Backstory")
    print("3) Update Level ")
    print("4) Update Gold")
    print("5) Update Inventory")
    print("6) Update Session Goals/Notes")
    print("7) Update Ability Scores")
    print("8) Save Character Changes and Return to Main Menu")
    print("9) Delete Character Permanently\n")

    while True:

      choice = input("Row Option: ").strip().lower()

      if choice == "1":   # ALIGNMENT
        print("Choose a row number from the following options. \nIf you need help deciding, type 'help' for a useful guide.\n")
        aligns = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]

        for a in range(0,9):
          print(f"{str(a+1)}) " + aligns[a])
        print()

        while True:
          choice = input("Alignment Option: ").strip().lower()
          
          try:
            if int(choice) > 0 and int(choice) < 10:
              CharObj.alignment = aligns[int(choice)-1]
              break
          except ValueError:
            if choice == "help":
              print("\n Opening: https://dnd5e.info/beyond-1st-level/alignment/#:~:text=A%20typical%20creature%20in%20the,%2C%20chaotic%2C%20or%20neutral).\n")
              wb.open("https://dnd5e.info/beyond-1st-level/alignment/#:~:text=A%20typical%20creature%20in%20the,%2C%20chaotic%2C%20or%20neutral).")
            else:
              print(f"I am sorry, I don't understand {choice}")
          except:
            print("Sorry, unable to open URL in browser.")
          break

      elif choice =="2":   # BACKSTORY
        while True:
          print("Write an interesting backstory for your character: \n")
          backstory = input()
          if backstory == '':
            print("Backstory can't be empty!")
          elif len(backstory) > 4000:
            print("Try cutting down the backstory to less than 4000 letters")
          else:
            CharObj.backStory = backstory
            break
          
      elif choice =="3": # LEVEL
        while True:
          lvl = input(f"What level is {CharObj.name}? (Remember that DND 5e levels range from 1 - 20): ").strip()
          try :
            if int(lvl) > 0 and int(lvl) < 21:
              CharObj.level = lvl
              break
            else:
              print("Character levels only range from 1 - 20")
          except:
            print(f"'{lvl}' is not a correct level entry. A correct entry is something like '1' or '15' ")

      elif choice =="4": # GOLD
        while True:
          gp = input(f"How many gold pieces does {CharObj.name} have: ").strip()
          try :
            if int(gp) > -1 and int(gp) < 10000000000000000000:
              CharObj.gold = gp
              break
            else:
              print("Gold entry cannot be negative nor can it be larger than 10000000000000000000")
          except:
            print(f"'{gp}' is not a correct gold entry. A correct entry is something like '10' or '150' ")

      elif choice =="5": # INVENTORY

        while True:
          print("Do you want to add or remove inventory items?\n")
          print("1) Add")
          print("2) Remove\n")

          choice = input("Inventory Option: ").strip()
          if choice == "1":

            while True:
              add = input(f"What would you like to add to {CharObj.name}'s inventory: ").strip()
              if add == '':
                print("You can't add nothing!")
              elif len(add) > 200:
                print("item description/name must be under 200 letters")
              else:
                CharObj.inventory.append(add)
                break

          elif choice == "2":
              
            if len(CharObj.inventory) == 0:
              print(f"There are no items in {CharObj.name}'s inventory")
              continue
            
            while True:
              print()
              for item in range (0,len(CharObj.inventory)):
                print(f"{str(item+1)}) {CharObj.inventory[item]}")
              print()

              choice = input(f"Which item would you like to remove from {CharObj.name}'s inventory? (Select a row number): ").strip()

              try:
                if int(choice) > 0 and int(choice) < (len(CharObj.inventory) + 1):
                  CharObj.inventory.pop(int(choice)-1)
                  break
                else:
                  print(f"'{choice}' is not a row number")
              except:
                print(f"'{choice}' is not a row number!")
          else:
            print(f"I don't understand '{choice}'\n")
        
          break

      elif choice=="6": # SESSION GOALS/NOTES

        while True:
          print("Do you want to add or remove session goals/notes?\n")
          print("1) Add")
          print("2) Remove\n")

          choice = input("Note Option: ").strip()
          if choice == "1":
            print("A good example of something to write is 'I curently have 5 health points' or 'sell magic staff')")
            while True:
              add = input(f"What note/goal would you like to add: ").strip()
              if add == '':
                print("You can't add nothing!")
              elif len(add) > 200:
                print("Note/goal description must be under 200 letters")
              else:
                CharObj.sessGoals.append(add)
                break

          elif choice == "2":
              
            if len(CharObj.sessGoals) == 0:
              print(f"There are no notes/goals for {CharObj.name}")
              continue
            
            while True:
              print()
              for item in range (0,len(CharObj.sessGoals)):
                print(f"{str(item+1)}) {CharObj.sessGoals[item]}")
              print()

              choice = input(f"Which note/goal would you like to remove? (Select a row number): ").strip()

              try:
                if int(choice) > 0 and int(choice) < (len(CharObj.sessGoals) + 1):
                  CharObj.sessGoals.pop(int(choice)-1)
                  break
                else:
                  print(f"'{choice}' is not a row number")
              except:
                print(f"'{choice}' is not a row number!")
          else:
            print(f"I don't understand '{choice}'\n")
        
          break


      elif choice =="7": # ABILITY SCORES
        while True:
          choice = input("Which ability score would you like to update? (i.e. 'Strength' or 'Charisma'): ").strip().lower()

          if choice.title() in CharObj.abScores.keys(): 
            val = input(f"What is the value of the new {choice.title()} score? (i.e. '5' or '16'): ")
            try:
              if int(val) > -1 and int(val) < 41:
                CharObj.abScores[choice.title()] = val
                break
              else:
                print("Score value can not be nagative nor can it exceed 40")
            except:
              print("You must type just a number (i.e. '5' or '16'")
          else:
            print(f"'{choice}' is not an ability score")
      elif choice =="8": # SAVE CHARACTER CHANGES
        print(f"\nGo forth, {CharObj.name}! \n\n")
        return CharObj
      elif choice =="9": # DELETE CHARACTER
        while True:
          choice = input(f"Are you absolutely sure you want to delete {CharObj.name} permanently? ('Y' for yes, 'N' for no): ").strip().lower()
          if choice == "y":
            print(f"\n Goodbye {CharObj.name}! \n")
            return choice
          elif choice == "n":
            break
          else:
            print(f"I am sorry, I don't understand '{choice}'\n")
      else:
        print(f"I did not understand '{choice}' ")
        continue

      break # re-display character info




def helpHeader(centerNum, text):
  '''
  Helper function to make headers easier
  '''
  
  print(10*" " + "+" + centerNum*"-" + "+")
  print(10*" " + "|" + f"{text}".center(centerNum) + "|")
  print(10*" " + "+" + centerNum*"-" + "+")



def sendChar():
  '''
  This will send characters to other users assuming they are calling recieveChar 
  '''

  try:
    shelfFile = shelve.open('.\DNP_Characters\Characters')
  except:
    print("You do not have any characters to send. Make a character and try again!\n")
    return 
  
  characterList = list(shelfFile.keys()) # list of keys which in this case are character names
  if len(characterList) == 0:
    print("You do not have any characters to send. Make a character and try again!\n")
    return
  
  print()
  for charNum in range(0,len(characterList)):
    print(f"{charNum+1}) {characterList[charNum]}") # prints out character names
  print()

  while True:
    choice = input("Which character would you like to send? (type a row number): ").strip()
    try:
      choice = int(choice)
      if choice > 0 and choice < (len(characterList)+1):
        CharObj = shelfFile[characterList[choice-1]]
        print("\nPlease type the appropriate ip address provided by the recieving user.")

        host = input("IP Address of reciever: ").strip()

        print("\nAttempting to connect...")

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
        try:
          client.connect((host, 1002))
        except:
          print("Connection attempt either failed or timed out. Double check ip address and try again.\n\n")
          break
        print(f"Connection made with other user! Sending {characterList[choice-1]}...")

        os.mkdir('.\DNP_Characters\Temp_Send')

        tempShelf = shelve.open('.\DNP_Characters\Temp_Send\Send')
        tempShelf[characterList[choice-1]] = CharObj
        tempShelf.close()


        # zip stuff

        # initializing empty file paths list
        file_paths = []

        # crawling through directory and subdirectories
        for root, directories, files in os.walk('.\DNP_Characters\Temp_Send'):
          for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)


        # printing the list of all files to be zipped
        '''
        print('Following files will be zipped:')
        for file_name in file_paths:
          print(file_name)
        '''


        # writing files to a zipfile
        with ZipFile('Send.zip','w') as zip:
          # writing each file one by one
          for file in file_paths:
            zip.write(file)
        


        file = open('.\Send.zip', 'rb')
        file_data = file.read(2048)
        while file_data:
          client.send(file_data)
          file_data = file.read(2048)
        file.close()
        


        client.close()
        print(f"Successful! Other user now has {characterList[choice-1]} added to their character list.\n\n")


        os.remove("send.zip")
        shutil.rmtree(".\DNP_Characters\Temp_Send")
        break
      else:
        print(f"'{choice}' is not a valid row number. Try again")
        continue
    except:
      print(f"'{choice}' is not a valid row number. Try again!")



def recieveChar():
  '''
  This will recieve characters to other users assuming they are calling sendChar 
  '''

  # In case the user does not have the shelf folder, make it for them
  try:
    shelfFile = shelve.open('.\DNP_Characters\Characters')
    shelfFile.close()
  except:
    os.mkdir('DNP_Characters') # in the event the user does not yet have a DNP_Characters folder
    shelfFile = shelve.open('.\DNP_Characters\Characters')
    shelfFile.close()


  print("\nIn order to receive a character from another user, you must provide your local wireless IP Address to the sender.")
  print("If you would like to proceed and begin awaiting the other user's character, enter 'proceed'")
  print("Otherwise enter 'exit' to return to the main menu.")
  print("\n(If you are unaware of your local IP Address, type 'help' and a list of your computer's IP Addresses will be provided to you.")
  print("IMPORTANT: you will need to specifically share the 'IPv4 Address' under the 'Wireless LAN adapter Wi-Fi' section)\n")

  

  while True:
    choice = input("Which would you like to do: ").strip().lower()

    if choice == "help":
      print()
      os.system("ipconfig")
      print()
    elif choice == "proceed":
      break
    elif choice == "exit":
      print()
      return
    else:
      print(f"I'm sorry, I didn't understand '{choice}' \n")

  host = ''
  port = 1002
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
  server.bind((host, port))  
  print("Awaiting to recieve character... (To cancel, close shellwindow)")
  server.listen()

  client_socket, client_address = server.accept()

  file = open('recv.zip', "wb")
  data_chunk = client_socket.recv(2048)  # stream-based protocol

  while data_chunk:
    file.write(data_chunk)
    data_chunk = client_socket.recv(2048)

  file.close()
  client_socket.close()
    
  # opening the zip file in READ mode
  with ZipFile("recv.zip", 'r') as zip:
    os.mkdir("Temp_Recv")
    zip.extractall(path=".\Temp_Recv")
  
  # open temporary shelve to obtain sent character
  tempShelf = shelve.open('.\Temp_Recv\DNP_Characters\Temp_Send\Send')

  # open permanent shelve in order to save sent character
  shelfFile = shelve.open('.\DNP_Characters\Characters')

  # list of recieved shelve from sender, will only contain the one character the sender provided
  temp_list = list(tempShelf.keys()) 

  # you can not recieve a character whose name is the same as an existing character the reciever already owns.
  # Since character names are the keys of the shelve, you must reject the sent character if there is a name match.
  if temp_list[0] in list(shelfFile.keys()):
    print(f"Unfortunately you already have a character named {temp_list[0]}, so the sent character will be rejected.\n\n")
  else: # Otherwise you are free to proceed
    print(f"Character has been recieved! Say hello to {temp_list[0]}!\n\n")

    # Finally, we copy the sent character over to the reciever's permanent shelve.
    shelfFile[temp_list[0]] = tempShelf[temp_list[0]]

  # Since we are finished with both shelves, we can close them now. 
  tempShelf.close()
  shelfFile.close()
  
  # The data recieved from the sender is no longer necessary and will be deleted.
  # The end user will never be able to notice the existance of these files because they will be used and discarded almost immediately.
  os.remove("recv.zip")
  shutil.rmtree(".\Temp_Recv")


    

  



#!!!!!!!!!!!!!!!!!!!!!!!!!!!! PROGRAM STARTS HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!

helpHeader(50,"Welcome to Dungeons and Pythons")


# Below is the Dungeons and Pythons mascot presented to the user at the beginning of every session.

print('''    

           /^\/^\					
         _|__|  O|					
\/     /~     \_/ \					
 \____|__________/  \					
        \_______      \					
                `\     \                 \		
                  |     |                  \		
                 /      /                    \		
                /     /                       \\\	
              /      /                         \ \	
             /     /                            \  \	
           /     /             _----_            \   \	
          /     /           _-~      ~-_         |   |	
         (      (        _-~    _--_    ~-_     _/   |	
          \      ~-____-~    _-~    ~-_    ~-_-~    /	
            ~-_           _-~          ~-_       _-~	
               ~--______-~                ~-___-~	          An adventure awaitsssss...


''')



# Beginning/Main DNP Menu ↓↓↓

while True:
    print(" + Enter '1' if you would like to make a new character.")
    print(" + Enter '2' if you would like to manage an existing character.")
    print(" + Enter '3' if you would like to send/recieve characters from other Dungeons and Pythons users. (WINDOWS USERS ONLY)")
    print(" + Enter 'exit' if you would like to leave the app.\n")
    choice = input("Which would you like to do: ").strip().lower()
    if choice == "1":
        print("\n")
        helpHeader(40, "Make a New Character")
        break
    elif choice == "2":
        print("\n")
        helpHeader(36, "Manage Your Characters")
        print()

        try:
          shelfFile = shelve.open('.\DNP_Characters\Characters')
        except:
          os.mkdir('DNP_Characters') # in the event the user does not yet have a DNP_Characters folder
          shelfFile = shelve.open('.\DNP_Characters\Characters')
        
        characterList = list(shelfFile.keys())
        if len(characterList) == 0:
          print("No characters have been created yet. Created characters will be stored in a folder called 'DNP_Characters' \n")
          continue

        for charNum in range(0,len(characterList)):
          print(f"{charNum+1}) {characterList[charNum]}")
        print()

        while True:
          choice = input("Which character would you like to manage? (type a row number): ").strip()
          try:
            choice = int(choice)
            if choice > 0 and choice < (len(characterList)+1):
              CharObj = shelfFile[characterList[choice-1]]
              break
            else:
              print(f"'{choice}' is not a valid row number. Try again")
              continue
          except:
            print(f"'{choice}' is not a valid row number. Try again!")
        
        helpHeader(36, f"Character: {CharObj.name}")
        print()
        
        nameSv = CharObj.name
        CharObj = characterManager(CharObj)   # Update Character

        if CharObj == "y":
          del shelfFile[nameSv]               # Delete Character
        else:
          shelfFile[CharObj.name] = CharObj   # Save Changes

        shelfFile.close()                     # Close Shelf
    elif choice == "3":
      print("\n")

      if platform.system() != "Windows":
        print("This feature is only offered for Windows users of Dungeons and Pythons, sorry!\n")
        continue

      helpHeader(30, "Character Share")
      print("\n")

      # Explaining the features of 'Character Share' to the user as well as some usage requirements
      print("This feature allows you to send or recieve characters to other Dungeons and Python users.")
      print("There are some requirements in order to use character sharing:")
      print("\t- The character being sent must not share a name with any character the reciever already owns.")
      print("\t- You and the other user must both be connected to the same Wifi network.")
      print("\t- The connection must be wireless (i.e. wired internet connection only will not work).")
      print("\t- A Windows notification may appear asking for you to enable python to allow for wireless connection access.")
      print("\t  In which case you must allow python to have said access in order to continue.\n")
      
      print("If you would like to proceed enter 'proceed', otherwise enter 'exit' to return to the previous menu.")
      while True:
        choice = input("Which would you like to do: ").strip().lower()
        if choice == "proceed":
          print()
          print("\t+ Enter '1' if you would like to send a character.")
          print("\t+ Enter '2' if you would like to recieve a character.\n")

          while True:
            choice = input("Which would you like to do: ").strip().lower()
            if choice == "1":
              sendChar()
              break
            elif choice == "2":
              recieveChar()
              break
            else:
              print(f"I'm sorry, I didn't understand '{choice}' \n")

          break
        elif choice == "exit":
          print('\n')
          break
        else:
          print(f"I'm sorry, I didn't understand '{choice}' \n")
      
      continue # return to main menu


    elif choice == "exit":
      exit()
    else:
      print(f"I'm sorry, I didn't understand '{choice}' \n")
        

# ---------------------------------- CHARACTER RACE I/O ----------------------------------

def pickRace():
  # list of possible races avaliable in Dungeons and Dragons 5th edition that the user can pick from
  races = ["Dragonborn","Dwarf","Elf","Gnome","Half-Elf","Halfling","Half-Orc","Human","Tiefling"]

  print("Let's start with your character's race. Choose from among these options:\n")

  # formatting the race options to the user
  for i in range(0,9):
    print(str(i+1) + ") " + races[i])

  print()
  print("If you would like to know more about a particular race before you make your choice, type 'info' below.")
  print("If you would like a race picked for you, type 'random' below.")
  print("Otherwise please just type the row number of the race you want your character to have below")
  while True:
      choice = input("\nRace Option: ").strip().lower()


      if choice == "info":

        while True:
          choice = input("\nWhich of the races would you like to know more about? \n(type a row number or 'none' to go back): ").strip().lower()
          if choice == 'none':
            break
          try: # if the user enters in something that is not an integer, the except clause will trigger
            # the user can only pick among the nine races available
            if int(choice) > 0 and int(choice) < 10:
              raceStr = races[int(choice)-1].lower()
              print("\nOpening:  https://www.dndbeyond.com/races/" + raceStr + "\n")
              try:
                wb.open('https://www.dndbeyond.com/races/' + raceStr)
              except:
                print("Sorry, unable to open URL in browser.")
              break
            else:
              print(f"'{choice}' is not a valid row number. Try again")
              print()
          except: # error was caught in try clause when the user's choice could not be converted to integer
            print(f"I'm sorry, I didn't understand '{choice}' ") # prompt user to try again
            continue
        continue # Go back to character race prompt

      elif choice == "random":
        # if the user wanted their character's race selected randomly
        choice = random.randrange(1,10)
      

      try:
        if int(choice) > 0 and int(choice) < 10:
          raceChoice = races[int(choice)-1]
          choice = input("Your character will be a " + raceChoice + " then? (Y/N): ").strip().lower()
          if choice == "y":
            return raceChoice
        else: 
          print(f"'{choice}' is not a valid row number. Try again")
      except:
        if choice != "info" and choice != "random":
          print(f"I'm sorry, I didn't understand '{choice}' ")

raceChoice = pickRace()
print()


# ---------------------------------- CHARACTER CLASS I/O ----------------------------------

def pickClass():
  classes = ["Barbarian","Bard","Cleric","Druid","Fighter","Monk","Paladin","Ranger","Rogue","Sorcerer","Warlock","Wizard"]

  print("Next is your character's class. Choose from among these options:\n")

  for i in range(0,12):
    print(str(i+1) + ") " + classes[i])

  print()
  print("If you would like to know more about a particular class before you make your choice, type 'info' below.")
  print("If you would like a class picked for you, type 'random' below.")
  print("Otherwise please just type the row number of the class you want your character to have below") 
  while True:
      choice = input("\nClass Option: ").strip().lower()


      if choice == "info":
        while True:
          choice = input("\nWhich of the classes would you like to know more about? \n(type a row number or 'none' to go back): ").strip().lower()
          if choice == 'none':
            break
          try:
            if int(choice) > 0 and int(choice) < 13:
              classStr = classes[int(choice)-1].lower()
              print("\nOpening:  https://www.dndbeyond.com/classes/" + classStr + "\n")
              try:
                wb.open('https://www.dndbeyond.com/classes/' + classStr)
              except:
                print("Sorry, unable to open URL in browser.")
              break
            else:
              print(f"'{choice}' is not a valid row number. Try again")
              print()
          except:
            print(f"I'm sorry, I didn't understand '{choice}' ")
            continue
        continue # Go back to character class prompt


      elif choice == "random": 
        choice = random.randrange(1,13)

      try:
        if int(choice) > 0 and int(choice) < 13:
          classChoice = classes[int(choice)-1]
          choice = input("Your character will be a " + classChoice + " then? (Y/N): ").strip().lower()
          if choice == "y":
            return classChoice
        else: 
          print(f"'{choice}' is not a valid row number. Try again")
          print()
      except:
        if choice != "info" and choice != "random":
          print("I'm sorry, I didn't understand.")

classChoice = pickClass()
print()


# ---------------------------------- ABILITY SCORE CALCULATIONS ----------------------------------


print("Now it's time to calculate ability score values! 6 values will be displayed down below.")
print("You will be asked which values will go to which of your character's ability score. \n")

def rollScores():

  values = []

  for score in range(1,7): # For each of the 6 scores
    rolls = []

    for roll in range(1,5): # roll 4 dice
      rolls.append(random.randrange(1,7))
    
    # Sum the highest 3 rolls 
    rolls.sort()
    sum = 0
    for i in range(1,4):
      sum += rolls[i]
    
    values.append(sum) # Add potential score to value list
  return values


while True:
  Scores = rollScores()

  for score in range(0,6):
    print(f"{score+1}) {Scores[score]}")
  print()

  choice = input("Would you like to re-roll your ability scores? (Y/N): ").strip().lower()
  if choice == "n":
    break
print()


def assignScores(Scores):
  abScores = {"Strength" : None, "Dexterity" : None, "Constitution" : None, "Intelligence" : None, "Wisdom" : None, "Charisma" : None}

  usedScores = []
  for ab in abScores.keys():

    while True: 
      print(f"Rows who's values have already been used: {usedScores}")
      choice = input(f"Which score would you like to go in {ab}? (select the row number): ").strip().lower()

      try:
        if choice in usedScores:
          print(f"you already used the score for row {choice}")
          print()
        elif int(choice) > 0 and int(choice) < 7:
          abScores[ab] = Scores[int(choice)-1]
          usedScores.append(choice)
          print()
          break
        else: 
          print(f"'{choice}' is not a valid row number. Try again")
          print()
      except:
        print(f"'{choice}' is not a valid row number. Try again!") 
        print()

  return abScores


while True:
  abScores = assignScores(Scores)
  print(f"Your character has the following ability scores: \n{abScores}")
  print()
  print("Are you satisfied with your ability scores?")
  choice = input("( 'Y' to move on / 'N' to reallocate scores): ").strip().lower()
  if choice == "y":
    break
  else:
      print()
      for score in range(0,6):
        print(f"{score+1}) {Scores[score]}")
      print()


# ---------------------------------- NAME, GENDER, AND AGE ASSIGNMENT ----------------------------------

def genderAssignment():

  print("\nWhat is your character's gender? \n")

  while True:
    print("1) Woman \n2) Man \n3) Ambiguous \n")  # Print out all of the options
    choice = input("Gender Option (please select row number): ").strip().lower() # Take in user input (guide them to type number)
    
    if choice == "1":
      genderChoice = "Woman"
      break
    elif choice == "2":
      genderChoice = "Man"
      break
    elif choice == "3":
      genderChoice = "Ambiguous"
      break
    else:
      print("I'm sorry, I didn't understand.")

  return genderChoice

while True:
  genderChoice = genderAssignment()
  choice = input(f"You went with the gender option: {genderChoice} \nIs this correct (Y/N): ").strip().lower()
  if choice == "y":
    break



def ageAssignment():
  print("\nHow old is your character?")
  print(f"In case you were wondering, here is some information about the lifespan of the {raceChoice} race:\n")

  try:  # Woohoo webscrapping...

    # Attempt to obtain data scrapped from website
    res = requests.get('http://dnd5e.wikidot.com/' + raceChoice.lower())
    res.raise_for_status()
    AgeSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    if raceChoice == 'Human' or raceChoice == 'Dragonborn':
      childNum = '1'
    elif raceChoice == 'Elf' or raceChoice == "Tiefling":
      childNum = '5'
    elif raceChoice == 'Half-Elf' or raceChoice == 'Half-Orc':
      childNum = '3'
    else:
      childNum = '2'
    elems = AgeSoup.select('#page-content > div.feature > div:nth-child(1) > div > ul:nth-child(' + childNum + ') > li')
    print('"' + elems[0].getText() + '"')
  except:
      print("Sorry, couldn't obtain information. You may want to check your internet connection.")

  while True:
    ageChoice = input("\nHow old would you like your character to be? (please enter a number of years): ").strip()
    try:
      if int(ageChoice) >= 0 and int(ageChoice) < 100000000:
        return ageChoice
      else:
        print(f"'{ageChoice}' is an invalid age")
    except:
      print("Your age must be in the form of a number like '5' '60' or '374'")


while True:
  ageChoice = ageAssignment()
  choice = input(f"So your character is {ageChoice} years old? \nIs this correct (Y/N): ").strip().lower()
  if choice == "y":
    break




print("\nNow let's give your character a name!")
print("If you would like, I can help you find some names based on your character's race and gender (just type 'help' below) ")

try:
  shelfFile = shelve.open('.\DNP_Characters\Characters') # Opened now to avoid conflicting names in shelve
except: 
  os.mkdir('DNP_Characters') # in the event the user does not yet have a DNP_Characters folder
  shelfFile = shelve.open('.\DNP_Characters\Characters')

def nameAssignment():
  while True:
    nameChoice = input("Name Option: ").strip()
    if nameChoice == '':
      print("\nYou must give your character a name!\n")
    elif nameChoice in shelfFile.keys():
      print(f"\nYou already have a character called {nameChoice}. You must use a new name!\n")
    elif nameChoice.lower() == 'help':

      print("\nOpening:  https://www.fantasynamegenerators.com/dnd-" + raceChoice.lower() + "-names.php" + "\n") # https://www.fantasynamegenerators.com/dnd-dragonborn-names.php
      try:
        wb.open("https://www.fantasynamegenerators.com/dnd-" + raceChoice.lower() + "-names.php")
      except:
        print("Sorry, unable to open URL in browser.")
      


    elif len(nameChoice) > 30:
      print("\nName must be less than 30 letters\n")
    else:
      return nameChoice

while True:
  nameChoice = nameAssignment()
  choice = input(f"Your character's name is {nameChoice}? (Y/N): ").strip().lower()
  if choice == "y":
    break



# ---------------------------------- CHARACTER FINALIZATION ----------------------------------

print()
helpHeader(40,"Character Finalization")

while True:

  print()
  print("This is your character:\n")
  print(f"1) Name: {nameChoice}")
  print(f"2) Gender: {genderChoice}")
  print(f"3) Race: {raceChoice}")
  print(f"4) Class: {classChoice}")
  print(f"5) Age: {ageChoice}")
  print(f"6) Ability Scores: \n   {abScores}")

  print("\nIf you are finished, type 'Y' below. Otherwise type the row number of what you would like to change\n")

  # Give the user the chance one last time to change anything they want about their character, or if they are finished.
  choice = input("Finalization Option: ").strip().lower() 
  if choice == "y":
    NewChar = Character(raceChoice, classChoice, nameChoice, ageChoice, genderChoice, abScores)
    
    # shelf opened in name creation to avoid conflicting names
    shelfFile[nameChoice] = NewChar
    shelfFile.close()

    print(f"{nameChoice} is now an established character! \nTo manage {nameChoice}'s information, restart DungeonsNPythons and select the manage existing character option!\nAll characters are stored in a folder called 'DNP_Characters' so do NOT delete that folder unless you want to lose all your characters!\n")
    break
  elif choice == "1":
    nameChoice = nameAssignment()
  elif choice == "2":
    genderChoice = genderAssignment()
  elif choice == "3":
    raceChoice = pickRace()
  elif choice == "4":
    classChoice = pickClass()
  elif choice == "5":
    ageChoice = ageAssignment()
  elif choice == "6":

    while True:
      Scores = rollScores()

      for score in range(0,6):
        print(f"{score+1}) {Scores[score]}")
      print()

      choice = input("Would you like to re-roll your ability scores? (Y/N): ").strip().lower()
      if choice == "n":
        break
    print()

    abScores = assignScores(Scores)
  else:
    print(f"I'm sorry, I didn't understand '{choice}' \n")


        
