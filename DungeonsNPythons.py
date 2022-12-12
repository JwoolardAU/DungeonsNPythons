# Code author: Patrick Woolard
# Email: Jwoolard@augusta.edu
# Github: https://github.com/JwoolardAU/DungeonsNPythons
# Information on Dungeons & Dragons/context on the app contents below: https://en.wikipedia.org/wiki/Dungeons_%26_Dragons


'''
Welcome to Dungeons & Pythons!

To run the app, just run 'python DungeonsNPythons.py' in the shell of your choosing.

Ensure that you have support for the following modules in your python environment:

- "requests" (For Webscrapping):     pip install requests
- "bs4" (Parses Webscrapped Data):   pip install bs4

Any other modules used should come already installed by default in your python installation

'''



#######  PROGRAM OVERVIEW  #######
'''
The general overview for the dungeons & pythons application code is as follows:

- importing all modules used in the application. Instructions have been provided on how to install modules that do not come with python by default above

- Defining a character class that contains all attributes a Dungeons & Dragons character needs

- Defining a character manager function 'characterManager' that allows the user to view and edit aspects of their character

- Defining a helper function 'helpHeader' that displays headerboxes in text to the user

- Defining a character sending function 'sendChar' that allows the user to send their characters to other dungeons & pythons users

- Defining a character receiving function 'receiveChar' that allows the user to receive characters from other dungeons & pythons users

- The Main() function then begins providing the user a text main menu for all the features offered in dungeons & pythons (character creation, character management, and character sharing)
  !!!!!! REMINDER: Main() in python is any code that does not exist within another defined function. Main() begins after the receiveChar() function definition.

- Main() continues so the user can use the character creation feature. For each step of character creation, we define a function (described below) to select and finalize character features.
  At the end of Main() the user finalizes their decisions on character creation, the character gets saved to an external file, and the app terminates.

- Defining a character race selection function 'pickRace'

- Defining a character class selection function 'pickClass'

- Defining an ability score dice rolling function 'rollScores'

- Defining an ability score allocation function 'assignScores'

- Defining a character gender selection function 'genderAssignment'

- Defining a character age selection function 'ageAssignment'

- Defining a character name selection function 'nameAssignment'
'''
##################################





# List of necessary modules used to execute Dungeons & Pythons:

import shelve # storing character information in dedicated shelve files (shelves operate as dictionaries in python) in a folder called 'DNP_Characters' so charachter infromation gets saved across multiple sessions
import random # mainly used for simulating rolling dice and creating values from random events
import webbrowser as wb # used to open up web browsers to give users more information about some aspect of Dungeons and Dragons
import requests # used to web scrape information off the internet to provide users with more helpful information when designing a character
import bs4 # useful tool to help parse and format web scrapped data
import os # use to handle file/folder control operations 
import platform # used to check operating system of user to prevent non-Windows users from crashing the app if they use 'Character Share' feature 
import socket # used to handle tcp communication for the 'Character Share' feature 
from zipfile import ZipFile # used to consolidate and extract shelve files for the 'Character Share' feature 
import shutil # only used to delete temporary directories created during 'Character Share' once they are no longer needed
import re # only used to create regular expressions filter to make obtaining personal ip address easier



# CLASS OVERVIEW:
# The Character class is used as a wrapper for all important details a Dungeons and Dragons character needs (i.e. race, class, ability scores, etc.)
# Each character object that gets created gets saved to a shelve so that saved characters exist across multiple sessions of the application
# The user can view and edit their character (and details thereof) in character management mode
class Character:
    
  # These get filled out in creation mode using constructor 
  # All except for abScores are strings. abScores is a dictionary that maps strings to integers
  race = None           
  charClass = None
  name = None
  age = None
  gender = None
  abScores = None # This one can be updated later in character management mode


  # Object constructor where we fill out class attributes based on user choices 
  # This will be called once the user has finalized their decision in main()
  def __init__(self, r, c, n, a, g, abS):
    '''
    EFFECTS: Creates character object based on all user decisions 

    REQUIRES: Each argument not be set to null
    '''
    self.race = r
    self.charClass = c
    self.name = n
    self.age = a
    self.gender = g
    self.abScores = abS
    self.sessGoals = []
    self.inventory = []


  # These get updated in character management mode. For now we set them to default values that get shown until the user updates them 
  # All are strings except for session goals (sessGoals) or inventory. Both of which are lists of strings
  level = "Not yet set... (Some campaigns require you start at higher levels)"
  gold = "0"
  alignment = "Not yet set... (your character's true nature may emerge as their adventures unfold)"
  sessGoals = None # If you have any goals or notes for the next play session (i.e. 'I curently have 5 health points' or 'sell magic staff') 
  inventory = None 
  backStory = "Not yet set... (Give your character a back story, it will help bring them more to life!)"



def characterManager(CharObj):
  '''
  EFFECTS: After the character is made, the user will use this to manage said character.
  The user selects a character in main() and it gets passed as CharObj. We return the updated character when the user decides to save.

  REQUIRES: CharObj is a valid character object that exists within the character shelve file

  MODIFIES: CharObj : Type 'Character'

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - while loop for handling user input about character managing options 
        - Present character information and character managing options 
        - If/else if branch for each option potential selected
            - Guide user through specified character feature update
        - Handle is user types in invalid update option
        - Return updated character object when user decides to select save option
    
  '''


  # User input validation loop. Options will be displayed for the user to pick from, and input will be validated in order to carry out commands.
  # Should the user type something the prompt did not ask for, they will be promted again.  
  while True:

    # Present all the information avaliable about the character selected (charObj)
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


    # Prompt the user to select an option to update character feature, save changes and return to main menu, or to delete character entirely. 
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

    # The user must pick a valid option from the choices above. Otherwise the user will be prompted again to pick a valid option.  
    while True:

      # Take the user input and remove extra unnecessary spacing
      choice = input("Row Option: ").strip()


      # Below is each choice branch where the user gets guided through their selected choice

      if choice == "1":   # ALIGNMENT 
        print("Choose a row number from the following options. \nIf you need help deciding, type 'help' for a useful guide.\n")

        # All of the alignment options avalible in Dungeons and Dragons
        aligns = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]

        # printing out all the alignment options for the user to pick from
        for a in range(0,9):
          print(f"{str(a+1)}) " + aligns[a]) # of the form '1) Lawful Good', '2) Neutral Good', etc. with a newline inbetween each listing
        print()

        # Alignment selection and input validation loop (each character feature update option has their own input validation loop)
        while True:
          # Take the user input and remove extra unnecessary spacing and lower case all alphabetical characters so that "Help", "HELP", "hElP", etc. are all valid
          choice = input("Alignment Option: ").strip().lower() 
          
          try: # if the user did not pick a number then casting the choice to int will crash 

            if int(choice) > 0 and int(choice) < 10: # The user can only pick an alignment option among the nine options that were presented to them previously
              CharObj.alignment = aligns[int(choice)-1] # Update the character object's alignment property to the choice the user selected 
              break # Break back into the main menu for character management where all character features (including the updated one) can be viewed

          except ValueError: # the user must not have typed a number meaning the casting the choice to an int threw a ValueError

            # Check to see if the user selected the help option
            if choice == "help":
              # If so, attempt to open a helpful guide on alignment in the user's default browser
              print("\n Opening: https://dnd5e.info/beyond-1st-level/alignment/#:~:text=A%20typical%20creature%20in%20the,%2C%20chaotic%2C%20or%20neutral).\n")
              wb.open("https://dnd5e.info/beyond-1st-level/alignment/#:~:text=A%20typical%20creature%20in%20the,%2C%20chaotic%2C%20or%20neutral).")
              continue # retun back to alignment option selection
            else: # The user did not type a valid alignment option 
              print(f"I am sorry, I don't understand {choice}")
              continue # retun back to alignment option selection
          except: # This will only trigger if the attempt to open guide in browser failed and threw an error (this may occur if the user is not connected to the internet for instance)
            print("Sorry, unable to open URL in browser.")
            continue # retun back to alignment option selection

      elif choice =="2":   # BACKSTORY
        while True: # The user can write a backstory for their character
          print("Write an interesting backstory for your character: \n")
          backstory = input()
          if backstory == '': # The user can not have an empty backstory
            print("Backstory can't be empty!")
          elif len(backstory) > 4000: # We limit the size of the character's backstory to 4000 characters
            print("Try cutting down the backstory to less than 4000 letters")
          else: # We update the character object's backstory to the one written by the user 
            CharObj.backStory = backstory
            break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
          
      elif choice =="3": # LEVEL
        while True:
          lvl = input(f"What level is {CharObj.name}? (Remember that DND 5e levels range from 1 - 20): ").strip()
          try : # The user can only type a value that is numeric, otherwise an exception will be thrown when casting their choice to an int
            if int(lvl) > 0 and int(lvl) < 21: # The user can only pick an level that is from 1 - 20 
              CharObj.level = lvl # We update the character object's level to the one written by the user 
              break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
            else: # The user can only pick an level that is from 1 - 20 
              print("Character levels only range from 1 - 20")
          except: # The user typed a level option that is not a number, so an exception was thrown when casting their choice to an int
            print(f"'{lvl}' is not a correct level entry. A correct entry is something like '1' or '15' ")

      elif choice =="4": # GOLD
        while True: 
          gp = input(f"How many gold pieces does {CharObj.name} have: ").strip()
          try : # The user can only type a value that is numeric, otherwise an exception will be thrown when casting choice to an int
            if int(gp) > -1 and int(gp) < 10000000000000000000: # The user can only give themselves 0 - 9999999999999999999 gold
              CharObj.gold = gp # We update the character object's gold amount to the one written by the user 
              break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
            else: # Tell the user their value entered was not a valid amount of gold
              print("Gold entry cannot be negative nor can it be larger than 10000000000000000000")
          except: # The user did not type a numeric value for gold. Inform them and let them try again
            print(f"'{gp}' is not a correct gold entry. A correct entry is something like '10' or '150' ")

      elif choice =="5": # INVENTORY

        # input validation loop for adding and removing items from character's inventory
        while True:
          # Present options
          print("Do you want to add or remove inventory items?\n")
          print("1) Add")
          print("2) Remove\n")

          choice = input("Inventory Option: ").strip()

          # User chose to add item to inventory
          if choice == "1":

            # validate that whatever the user wishes to add is not nothing (i.e. '') or something that exceeds 200 characters to describe
            while True:
              add = input(f"What would you like to add to {CharObj.name}'s inventory: ").strip()
              if add == '':
                print("You can't add nothing!")
              elif len(add) > 200:
                print("item description/name must be under 200 letters")
              else:
                CharObj.inventory.append(add) # append whatever item the user typed to the character object's inventory list
                break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
          
          # User chose to remove item from inventory
          elif choice == "2":
              
            # Infrom the user they can not remove items if their list is already empty
            if len(CharObj.inventory) == 0:
              print(f"There are no items in {CharObj.name}'s inventory")
              continue
            
            # If the character list is not empty, print out each item in the character's inventory list as an option to be removed
            # Options will look like "1) Magic Sword", "2) Health Potion", etc.
            while True:
              print()
              for item in range (0,len(CharObj.inventory)):
                print(f"{str(item+1)}) {CharObj.inventory[item]}")
              print()

              choice = input(f"Which item would you like to remove from {CharObj.name}'s inventory? (Select a row number): ").strip()

              # Let the user select one of the items to remove that was presented as an option previously
              try: # The user can only type a numeric value as a choice otherwise, when casting to an int, an exception will be thrown
                if int(choice) > 0 and int(choice) < (len(CharObj.inventory) + 1): # The user can only type a number that was presented as an item option previously
                  CharObj.inventory.pop(int(choice)-1) # remove the inventory item from the list that was associated with the option number the user typed/selected.
                  break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
                else: # The user typed an invalid row number option. Let user try again.
                  print(f"'{choice}' is not a row number")
              except: # The user typed something that was not numeric, causing an exception when the int casting occured. Let user try again.
                print(f"'{choice}' is not a row number!")

          # The user chose something that was neither the option to add nor remove inventory items. Inform them and let them try again. 
          else:
            print(f"I don't understand '{choice}'\n")
        
          break

      elif choice=="6": # SESSION GOALS/NOTES

        # input validation loop for adding and removing session goals/notes from character's session goals/notes list
        while True:
          print("Do you want to add or remove session goals/notes?\n")
          print("1) Add")
          print("2) Remove\n")

          choice = input("Note Option: ").strip()

          # User chose to add a session goal/note
          if choice == "1":
            print("A good example of something to write is 'I curently have 5 health points' or 'sell magic staff')")

            # validate that whatever the user wishes to add is not nothing (i.e. '') or something that exceeds 200 characters to describe
            while True: 
              add = input(f"What note/goal would you like to add: ").strip()
              if add == '':
                print("You can't add nothing!")
              elif len(add) > 200:
                print("Note/goal description must be under 200 letters")
              else:
                CharObj.sessGoals.append(add) # append whatever goal/note the user typed to the character object's session goals/notes list
                break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
          
          # User chose to remove a session goal/note
          elif choice == "2":
            
            # Infrom the user they can not remove goals/notes if their list is already empty  
            if len(CharObj.sessGoals) == 0:
              print(f"There are no notes/goals for {CharObj.name}")
              continue
            
            # If the character list is not empty, print out each goal/note in the character's session goals/notes list as an option to be removed
            # Options will look like "1) Talk to wizard", "2) Sell magic staff", etc.
            while True:
              print()
              for item in range (0,len(CharObj.sessGoals)):
                print(f"{str(item+1)}) {CharObj.sessGoals[item]}")
              print()

              choice = input(f"Which note/goal would you like to remove? (Select a row number): ").strip()

              # Let the user select one of the notes/goals to remove that was presented as an option previously
              try: # The user can only type a numeric value as a choice otherwise, when casting to an int, an exception will be thrown
                if int(choice) > 0 and int(choice) < (len(CharObj.sessGoals) + 1): # The user can only type a number that was presented as a goal/note option previously
                  CharObj.sessGoals.pop(int(choice)-1) # remove the goal/note from the list that was associated with the option number the user typed/selected.
                  break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
                else: # The user typed an invalid row number option. Let user try again.
                  print(f"'{choice}' is not a row number")
              except: # The user typed something that was not numeric, causing an exception when the int casting occured. Let user try again.
                print(f"'{choice}' is not a row number!")

          # The user chose something that was neither the option to add nor remove session goal/note. Inform them and let them try again. 
          else:
            print(f"I don't understand '{choice}'\n")
        
          break


      elif choice =="7": # ABILITY SCORES

        # input validation loop for updating character object's ability scores dictionary
        while True:
          # user input is stripped of extra spacing at beginning and end and all alphabetical characters are made lower case
          # This done to make matching with ability keys of the dictionary even easier 
          choice = input("Which ability score would you like to update? (i.e. 'Strength' or 'Charisma'): ").strip().lower()

          # The user must pick a valid Dungeons & Dragons ability. It is assumed the player will know each of the six abilities ahead of time (it is a fundamental part of the game)
          if choice.title() in CharObj.abScores.keys(): 
            val = input(f"What is the value of the new {choice.title()} score? (i.e. '5' or '16'): ")
            try: # The user must type something numeric otherwise the casting of val to int will cause an exception
              if int(val) > -1 and int(val) < 41: # The user can only assign scores whose value fall within the range of 0 to 40
                CharObj.abScores[choice.title()] = val # Assign ability score to the value typed in by the user
                break # Break back into the main menu for character management where all character features (including the updated one) can be viewed
              else: # The user attempted to assign a score that did not fall within the valid range. Infrom them and let them try again. 
                print("Score value can not be nagative nor can it exceed 40")
            except: # The user did not type a numeric value as score. Infrom them and let them try again. 
              print("You must type just a number (i.e. '5' or '16'")
          else: # The user typed in an ability that is not valid. Infrom them and let them try again. 
            print(f"'{choice}' is not an ability score")

      elif choice =="8": # SAVE CHARACTER CHANGES
        print(f"\nGo forth, {CharObj.name}! \n\n")

        # Return the updated character object back to main() where it will be saved to the shelve folder
        return CharObj

      elif choice =="9": # DELETE CHARACTER
        while True: # Make sure the user is completely sure they want to delete the character
          choice = input(f"Are you absolutely sure you want to delete {CharObj.name} permanently? ('Y' for yes, 'N' for no): ").strip().lower()
          if choice == "y":
            print(f"\n Goodbye {CharObj.name}! \n")

            # In this case, we will be returning the flag value of "y" back to main() which signals that this specific character object needs to be deleted from the shelve folder permanently
            return choice 
          elif choice == "n": # if they are not sure then just return them back to the main menu for character management
            break
          else: # If the user did not type the appropriate yes or no command, infrom the user and let them try again.
            print(f"I am sorry, I don't understand '{choice}'\n")

      else: # The user did not choose a valid choice for updating their character, saving, or deleting. Infrom them and let them try again
        print(f"I did not understand '{choice}' ")
        continue

      break # re-display character info




def helpHeader(centerNum, text):
  '''
  EFFECTS: Helper function that makes displaying headers easier for each feature of the application, for example:

  +------------------------------------+
  |       Manage Your Characters       |
  +------------------------------------+

  The text argument is the text that goes in the box, and the centerNum argument is what decides how wide the box should be. 

  REQUIRES: text must not be null and centerNum must be a positive integer

  HELPS: Main()
  '''
  
  print(10*" " + "+" + centerNum*"-" + "+")                   # start 10 spaces to the right of the terminal, add a '+', then centerNum number of '-', and another '+'
  print(10*" " + "|" + f"{text}".center(centerNum) + "|")     # start 10 spaces to the right of the terminal, add a '|', then center the text with respect to centerNum, and another '|'
  print(10*" " + "+" + centerNum*"-" + "+")                   # start 10 spaces to the right of the terminal, add a '+', then centerNum number of '-', and another '+'



def sendChar():
  '''
  EFFECTS: This will send a selected character (more specifically a character object) to another dungeons & pythons user 

  REQUIRES: The other dungeons & pythons user must have selected the 'Character Share' feature and are pending character receiving

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Open permanent character shelve/dictionary and let user pick character they wish to send (validate input in while loop as needed)
        - Obtain receiving user's IP Address from user
        - Create client socket object that will be used to send character object using tcp protocol
        - Connect client (sender) to host (receiver) 
        - If connection fails then inform user
        - Otherwise create temporary shelve file/folder for the character that was selected
        - Then create a zip file of the temporary shelve folder
        - send zip file data to receiver in chunks until entire file is sent (using a while loop)
        - Terminate connection to host and delete temporary shelve and zip file
        - Close permanent shelve
    - Inform the user if they made in mistakes when selecting a character or entering host's IP address
  '''

  # Check to see if there is a character shelve
  try:
    shelfFile = shelve.open('.\DNP_Characters\Characters')
  except:
    #if there isn't, prompt the user to make characters and exit the sending procedure
    print("You do not have any characters to send. Make a character and try again!\n")
    return 
  
  characterList = list(shelfFile.keys()) # list of keys which in this case are character names

  # check to see if the user has any characters to send. If not, then exit the sending procedure
  if len(characterList) == 0:
    print("You do not have any characters to send. Make a character and try again!\n")
    return
  
  # prints out all character names as options for sending
  # Options will look like "1) Patrick ", "2) Paul", "3) Sarah", etc.
  print()
  for charNum in range(0,len(characterList)):
    print(f"{charNum+1}) {characterList[charNum]}") 
  print()

  # User selection and input validation loop
  while True:

    choice = input("Which character would you like to send? (type a row number): ").strip()

    try: # in case the user enters a non numeric value, the except clause will trigger
      choice = int(choice)
      if choice > 0 and choice < (len(characterList)+1): # the user can only pick an integer that corresponds with a character option that was provided previously

        # Obtain the user's selected character object from shelve
        CharObj = shelfFile[characterList[choice-1]]

        # Now the user must enter in the recieving user's IP Address
        print("\nPlease type the appropriate ip address provided by the recieving user.")

        # Obtain input from user that should be the IP Address of the reciever 
        host = input("IP Address of reciever: ").strip()

        # Infrom user that the application is attempting to connect to the reciever
        print("\nAttempting to connect...")

        # This creates the socket object that will send the character object to the other user using tcp protocol over a shared local network connection
        # The arguments correspond with the protocols we wish to use for communication, i.e. TCP/IP (AF_INET = IP, SOCK_STREAM = TCP)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

        # If the user entered the wrong IP or anything else that doesn't make sense, the execpt clause will trigger 
        try:
          # Try to connect to the recieving user
          client.connect((host, 1002))
        except:
          # Connection failed and we exit the sending procedure
          print("Connection attempt either failed or timed out. Double check ip address and try again.\n\n")
          break # This returns the user back to the main menu

        # Alert user the connection was successful and that the character selected will be sent
        print(f"Connection made with other user! Sending {characterList[choice-1]}...")

        # Make a temporary directory for storing a temporary shelve that... 
        os.mkdir('.\DNP_Characters\Temp_Send')

        # ... contains only the character object the user wishes to send
        tempShelf = shelve.open('.\DNP_Characters\Temp_Send\Send')
        tempShelf[characterList[choice-1]] = CharObj
        tempShelf.close()


        # For ease of implementation, we will be sending all of the shelve files (of which there are 3 for a given shelve object)
        # as one zipped folder/file. The reason for this is because sending multiple files using the client object above can be rather
        # tedious as far as separating and assembling the files' data into their distinct files on the recieving end. So we send everything
        # as one zipped folder/file instead, and extract all of the contents on the recieving end.

        # initializing empty file paths list (we need to collect the path of all files we wish to collect)
        file_paths = []

        # crawling through the temporary directory to collect all file paths 
        # os.walk() is an easy way to access all of the directory's files and root path information
        # root is the full path to the Temp_Send directory and files is a list of each file in the Temp_Send directory.
        # There is only one directory of interest (Temp_Send), meaning 'directories' is not used and should just be ignored
        for root, directories, files in os.walk('.\DNP_Characters\Temp_Send'): 
          for filename in files:
            # join the two strings root and filename in order to form the full filepath to the shelve file.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath) # append the shelve file path to the shelve file_paths list


        # printing the list of all files to be zipped (for testing purposes only)
        '''
        print('Following files will be zipped:')
        for file_name in file_paths:
          print(file_name)
        '''


        # Writing all files whose paths we collected above to a zipfile
        with ZipFile('Send.zip','w') as zip:
          # Writing each file one by one
          for file in file_paths:
            zip.write(file)
        

        # Now that we have our one unified zipfile, we write its data to the recieving user
        file = open('.\Send.zip', 'rb')
        file_data = file.read(2048) # We will be sending the zip file in 2048 byte chunks...
        # ... until there is no more data to send (in which case file_data will be None which the while loop evaluates as false)
        while file_data:
          client.send(file_data) # send file data to recieving user
          file_data = file.read(2048) # grab the next 2048 byte chunk
        file.close() # The zip file has been sent completely and can now be closed
        

        # We are finished with our connection to the other user so we terminate it
        client.close()

        # Inform the user the sending was successful
        print(f"Successful! Other user now has {characterList[choice-1]} added to their character list.\n\n")

        # The zipfile and the temporary shleve directory (and its contents) are no longer needed so we delete them
        # The end user should never even know they existed
        os.remove("send.zip") # deletes zip file
        shutil.rmtree(".\DNP_Characters\Temp_Send") # deletes Temp_Send directory and all of its contents
        break
      
      else: # The user entered an integer choice that was not valid. Prompt them to try again
        print(f"'{choice}' is not a valid row number. Try again")
        continue
    except: # The user entered something that was not an integer causing `int(choice)` to throw an error. Prompt them to try again
      print(f"'{choice}' is not a valid row number. Try again!")



def receiveChar():
  '''
  EFFECTS: This will receive a character (more specifically a character object) from another another dungeons & pythons user

  REQUIRES: The other dungeons & pythons user must have selected the 'Character Share' feature and are pending character sending

  MODIFIES: Permanent character shelve file/dictionary

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Open character shelve/dictionary and let user confirm if they want to proceed with character receiving, exit back to main , or print out their local IP address (validate input in while loop as needed)
        - If the user chose to see their local IP address...
            - pipe 'ipconfig' shell command results into external text file.
            - use regular expressions to find exact line of information about local IP address and print it 
            - delete text file containing 'ipconfig' shell command results since it is no longer needed
        - If the user made a mistake typing a choice, inform them and let them try again.
        - Otherwise create host socket object that will be used to receive character object using tcp protocol
        - Connect client (sender) to host (receiver) 
        - If connection fails then inform user
        - Otherwise write received data in chunks to zip file until all data has been received (using a while loop)
        - Terminate connection to client
        - Extract all contents to a temporary folder and open shelve from contents (which is the one character sent by client)
        - Check to see if there is a character that exists in the permanent shelve that shares the same name as the character received
        - Reject character if there is a name match, otherwise save character in temporary shelve to permanent shelve
        - Close permanent shelve and delete temporary shelve and zip file
  '''

  # In case the user does not have the shelve folder, make it for them
  try: # if we try to open a file that does not exist, then an exception will be thrown
    shelfFile = shelve.open('.\DNP_Characters\Characters')
    shelfFile.close() # If the file opens successfully then that means it exists and we need not do anything else except close the file
  except:  # an exception was thrown trying to open a file that does not exist so meaning the user does not yet have a DNP_Characters folder
    os.mkdir('DNP_Characters') # In which case we make the folder for the user and create the shelve file
    shelfFile = shelve.open('.\DNP_Characters\Characters')
    shelfFile.close() # Nothing to do just yet so we close the file


  # Inform the user on providing the proper IP Address needed for communication to the sending user
  print("\nIn order to receive a character from another user, you must provide your local wireless IP Address to the sender.")
  print("If you would like to proceed and begin awaiting the other user's character, enter 'proceed'")
  print("Otherwise enter 'exit' to return to the main menu.")
  print("\n(If you are unaware of your local IP Address, type 'help' and it will be provided to you.\n")

  
  # User selection and input validation loop
  while True:
    choice = input("Which would you like to do: ").strip().lower()

    if choice == "help": # In the event the user does not know their IP Address, we can print out the information to the shell for the user to obtain
      print()

      # We can utilize regular expressions to parse and provide the correct individual IP Address.
      # We start by piping IP Address information to temporary text file called stuff.txt
      os.system("ipconfig >> stuff.txt") 

      # Temporary file containing IP Address information
      with open('stuff.txt', 'r') as file:
        data = file.read() # put results of ipconfig command into data variable 

      # Regex filter to find correct ipv4 adress:
      # x is a list of strings that match the regex below (it searches for the wifi specific ip address in data)
      x = re.findall("Wireless LAN adapter Wi-Fi:\n*.*\n*.*\n*.*", data) 

      # Printing the correct address to the user to share:
      # x should only contain one string that matches the regex (hence why we access x[0])
      # We only want the portion of that string (x[0][...]) that contains the IPv4 address information.
      # We find that by grabing the index of the string starting from where IPv4 is mentioned (x[0].index('IPv4'))
      # all the way to the end of the string (the : following x[0].index('IPv4'))
      try: # If for some reason the regex fails to capture string correctly we will catch any exceptions that may arise.
        print(x[0][x[0].index('IPv4'):])
      except: # Tell the user that they will have to look up their IP Address manually since the automatic retrieval failed
        print("Unfortunately we were unable to locate your IP address for you. You can look it up manually using the command 'ipconfig' in a different shell.")

      # The temporary file is no longer needed so we can delete it
      os.remove("stuff.txt") 
      print()
    elif choice == "proceed": # The user wishes to proceed to character receiving 
      break
    elif choice == "exit": # The user wants to return back to the main menu
      print()
      return
    else: # The user typed something that was not a valid option. Infrom them and let them try again.
      print(f"I'm sorry, I didn't understand '{choice}' \n")

  # Server (receiving user) creation:

  # This is the IP address the sending user will be hosted on. 
  # It being blank signifies that it will be open to any client IP address (the sending user) that wishes to connect to it on the specified port below. 
  host = '' 

  # The port number the host will be listening out for the sending user on.
  # The port value has been chosen mostly arbitrarily and is hardcoded to match the sending user's port. The user can not access nor change this.
  port = 1002 

  # This creates the socket object that will recieve the character object from the other user using tcp protocol over a shared local network connection.
  # The arguments correspond with the protocols we wish to use for communication, i.e. TCP/IP
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
  server.bind((host, port))  # bind server to IP and port above

  # keyboard shutdown (CRTL+C) does not work. If user needs to restart, they must close the shell and restart the app manually.
  # This is due to the implementation of the listen method for the server object
  print("Awaiting to recieve character... (To cancel, close shellwindow)") 

  try:
    server.listen() # Await connection from other user
  except: 
    
    # If for some reason the listen method fails, we will handle the exception here. This should never occur, but just in case to prevent the application from crashing, we will...
    # ... catch the exception, prompt the user to try again, and return them to the main menu
    print("Server failure. Try again\n\n")
    return

  # server (reciever) has successfully established client (sender) connection
  client_socket, client_address = server.accept()

  # We expect that the user is sending a zip file, so we will create one from the data being recieved
  file = open('recv.zip', "wb")

  # We will be recieving data for the zip file in 2048 byte chunks
  data_chunk = client_socket.recv(2048)  # this is the first 2048 byte chunk

  # When we run out of data chunks to write to the zip file the loop will terminate
  while data_chunk:
    file.write(data_chunk) # Write the data chunk to the file
    data_chunk = client_socket.recv(2048) # Collect the next data chunk

  # Close zipfile and terminate connection to client (sender)
  file.close()
  client_socket.close()

  # extracting the contents of the recieved zip file to a temporary directory called Temp_Recv 
  with ZipFile("recv.zip", 'r') as zip:
    os.mkdir("Temp_Recv")
    zip.extractall(path=".\Temp_Recv")
  
  # open temporary shelve to obtain sent character
  tempShelf = shelve.open('.\Temp_Recv\DNP_Characters\Temp_Send\Send')

  # open the usual permanent shelve in order to save sent character
  shelfFile = shelve.open('.\DNP_Characters\Characters')

  # list of recieved shelve keys (character names) from sender, will only contain the one character the sender provided (i.e. temp_list[0])
  temp_list = list(tempShelf.keys()) 

  # you can not recieve a character whose name is the same as an existing character the reciever already owns.
  # Since character names are the keys of the shelve, you must reject the sent character if there is a name match.
  if temp_list[0] in list(shelfFile.keys()): # Check if user already has character of the same name as recieved character
    print(f"Unfortunately you already have a character named {temp_list[0]}, so the sent character will be rejected.\n\n")
  else: # Otherwise you are free to proceed
    print(f"Character has been recieved! Say hello to {temp_list[0]}!\n\n")

    # Finally, we copy the sent character over to the reciever's permanent shelve.
    shelfFile[temp_list[0]] = tempShelf[temp_list[0]]

  # Since we are finished with both shelves, we can close them now. 
  tempShelf.close()
  shelfFile.close()
  
  # The data recieved from the sender (the recv.zip file) is no longer necessary and will be deleted. Same goes for the temporary shelve folder Temp_Recv
  # The end user will never be able to notice the existance of these files because they will be used and discarded almost immediately.
  os.remove("recv.zip")
  shutil.rmtree(".\Temp_Recv")


    

  


#!!!!!!!!!!!!!!!!!!!!!!!!!!!! PROGRAM/Main() STARTS HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!


helpHeader(50,"Welcome to Dungeons and Pythons") # Greet user with welcome header


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



# ↓↓↓ Beginning/Main DNP Menu ↓↓↓

# This acts as the main menu option execution and input validation loop
while True:

  # present user with their primary options
  print(" + Enter '1' if you would like to make a new character.")
  print(" + Enter '2' if you would like to manage an existing character.")
  print(" + Enter '3' if you would like to send/recieve characters from other Dungeons and Pythons users. (WINDOWS USERS ONLY)")
  print(" + Enter 'exit' if you would like to leave the app.\n")

  # Throughout the program input will be validated for user ease-of-use and to prevent logic/programmatic errors
  # strip() will remove unncessary spacing at the beginning and end of string variables. Example: "   Patrick  " is just "Patrick"
  # lower() will turn every alphabetic character to lowercase if it is not already. Example "Patrick","PATRICK", and "pAtRiCk" all become "patrick"
  choice = input("Which would you like to do: ").strip().lower() 

  if choice == "1": # This option begins the character creation sequence down below main menu while loop
      print("\n")
      helpHeader(40, "Make a New Character") # display character creation header
      break # breaks out of main menu while loop and begins character creation sequence

  elif choice == "2": # This option opens the character manager, allowing the user to view/edit existing character information
      print("\n")
      helpHeader(36, "Manage Your Characters") # display character manager header
      print()

      # Try to open character shelve to access saved characters. If the user does not have a shelve, an exception will be thrown signaling for one to be created
      try:
        shelfFile = shelve.open('.\DNP_Characters\Characters')
      except:
        # in the event the user does not yet have a shelve...
        os.mkdir('DNP_Characters') # ... we create the folder it will go in...
        shelfFile = shelve.open('.\DNP_Characters\Characters') # ... and create and open a new shelve.
      
      # Store the characters' names from shelve as a list. Remember that shelves operate the same as dictionaries in python.
      characterList = list(shelfFile.keys())

      # Check to see if the user has any characters. If they do not, inform them and return to main menu
      if len(characterList) == 0:
        print("No characters have been created yet. Created characters will be stored in a folder called 'DNP_Characters' \n")
        continue

      # Format and present character options for user to manage
      # Options will look like "1) Patrick ", "2) Paul", "3) Sarah", etc.
      for charNum in range(0,len(characterList)):
        print(f"{charNum+1}) {characterList[charNum]}")
      print()

      # User character option selection and input validation loop
      while True:
        choice = input("Which character would you like to manage? (type a row number): ").strip()
        try: # if the user does not type a numeric value, then the following conversion will throw
          choice = int(choice) 
          if choice > 0 and choice < (len(characterList)+1): # The user picked a valid character option among those presented previously
            # Obtain the appropriate character object from shelve
            CharObj = shelfFile[characterList[choice-1]]
            break # Break out of character option selection and input validation loop and proceed to character manager
          else: # The user did not type in a valid option among those presented previously. Infrom them and let them try again.
            print(f"'{choice}' is not a valid row number. Try again")
            continue
        except: # The user typed a value that was not numeric. Infrom them and let them try again.
          print(f"'{choice}' is not a valid row number. Try again!")
      
      helpHeader(36, f"Character: {CharObj.name}") # display character name header
      print()
      
      nameSv = CharObj.name # save character name in case user chooses to delete the character from shelve 
      CharObj = characterManager(CharObj)   # Update Character Object

      if CharObj == "y": # characterManager() will return just "y" as a flag to signal that the user wanted to delete the character they chose. 
        del shelfFile[nameSv]               # Delete Character
      else: # Otherwise we update the character object stored in shelve to the character object that returned after being updated in characterManager() 
        shelfFile[CharObj.name] = CharObj   # Save Changes

      shelfFile.close()                     # Close Shelf
  elif choice == "3": # This option allows users to share characters with one another
    print("\n")

    # prevent user from character share feature if they are not on a windows operating system
    # (The main reason for this is the execution of windows only shell commands in the "Character Share" feature will crash on any other platform)
    if platform.system() != "Windows":
      print("This feature is only offered for Windows users of Dungeons and Pythons, sorry!\n")
      continue

    helpHeader(30, "Character Share") # display character share header
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

    # User proceed/exit selection and input validation loop
    while True:
      choice = input("Which would you like to do: ").strip().lower()

      # The user chose to proceed with character sharing and will now pick whether to send or recieve a character
      if choice == "proceed":
        print()
        print("\t+ Enter '1' if you would like to send a character.")
        print("\t+ Enter '2' if you would like to recieve a character.\n")

        # User send/recieve selection and input validation loop
        while True:
          choice = input("Which would you like to do: ").strip().lower()
          if choice == "1": # begin the sending procedure
            sendChar()
            break # Return back to main menu loop
          elif choice == "2": # begin the recieving procedure
            receiveChar()
            break # Return back to main menu loop
          else: # The user typed an invalid option. Inform them and try again. 
            print(f"I'm sorry, I didn't understand '{choice}' \n")

        break
      elif choice == "exit": # The user does not want to character share and will return to the main menu loop
        print('\n')
        break
      else: # The user typed an invalid option. Inform them and try again. 
        print(f"I'm sorry, I didn't understand '{choice}' \n")
    
    continue # return to main menu (the outer most while loop)


  # user has finished their session and wishes to exit the program peacefully
  elif choice == "exit":
    exit()
  else: # user entered in something that was not a valid choice
    print(f"I'm sorry, I didn't understand '{choice}' \n")
        


# ↓↓↓ CHARACTER CREATION STARTS HERE ↓↓↓

# Character creation utilizes functions made to create and validate aspects of a Dungeons and Dragons character.
# These aspects were made into functions to be re-utlized as needed when the user finializes their decisions when making a character
# and when using the "Character Manager" feature.


# ---------------------------------- CHARACTER RACE I/O ----------------------------------

def pickRace():
  '''
  EFFECTS: Returns a valid race choice (as string) for a Dungeons & Dragons character. Also helps provide the user with more information about a
  particular race should they wish to know more and the ability for the user to pick the race at random.

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Print out all possible race options to user and let user know they can select a race randomly, or they can find out more about a particular race
    - Validate user input using while loop and input if/elif/else checks
        - If the user chose to find out more about a race then...
            - Use another while loop to validate input on which race they would like to know more about
                - open up web page in their default browser on the race they wanted to know more about
                - if this fails, catch the exception and inform user
        - If the user chose to pick their race randomly, then use random number generator to pick number associated with race option
        - If the user chose to pick a race option, then confirm the user's choice and return string of race that was associated with the number race option the user chose
        - Otherwise if the user made a mistake making a selection, then inform the user and let them try again
  '''


  # list of possible races avaliable in Dungeons and Dragons 5th edition that the user can pick from
  races = ["Dragonborn","Dwarf","Elf","Gnome","Half-Elf","Halfling","Half-Orc","Human","Tiefling"]

  print("Let's start with your character's race. Choose from among these options:\n")

  # formatting the race options to the user
  # Options will look like "1) Dragonborn ", "2) Dwarf", etc.
  for i in range(0,9):
    print(str(i+1) + ") " + races[i])

  print()
  print("If you would like to know more about a particular race before you make your choice, type 'info' below.")
  print("If you would like a race picked for you, type 'random' below.")
  print("Otherwise please just type the row number of the race you want your character to have below")

  # User race option selection and input validation loop
  while True:
      choice = input("\nRace Option: ").strip().lower()

      # Should the user want to know more about a class
      if choice == "info":

        # User race option information selection and input validation loop
        while True:
          choice = input("\nWhich of the races would you like to know more about? \n(type a row number or 'none' to go back): ").strip().lower()
          if choice == 'none': # The user is done wanting more information and will return back to the race option selection loop
            break
          try: # if the user enters in something that is not a numeric value, the except clause will trigger
            
            if int(choice) > 0 and int(choice) < 10: # the user can only pick among the nine races available
              raceStr = races[int(choice)-1].lower() # save the race the user picked as a string
              print("\nOpening:  https://www.dndbeyond.com/races/" + raceStr + "\n")
              try:
                # the user's default web browser will open displaying a page about the race option they want to learn more about
                wb.open('https://www.dndbeyond.com/races/' + raceStr)
              except: # If for some reason opening the link fails
                print("Sorry, unable to open URL in browser.")
              break # return back to the race option selection loop
            else:# The user typed something that was not a valid race option number
              print(f"'{choice}' is not a valid row number. Try again")
              print()
          except: # error was caught in try clause when the user's choice could not be converted to integer
            print(f"I'm sorry, I didn't understand '{choice}' ") # prompt user to try again
            continue
        continue # Go back to character race prompt

      elif choice == "random":
        # if the user wanted their character's race selected randomly, then assign a race option number randomly
        choice = random.randrange(1,10)# randrange returns integer between inclusive lower bound and exclusive upper bound
      
      
      try: # if the user enters in something that is not a numeric value, the except clause will trigger
          
        if int(choice) > 0 and int(choice) < 10: # the user can only pick among the nine races available
          raceChoice = races[int(choice)-1] # save the race the user picked as a string

          # Confirm that user is okay with the race option they selected
          choice = input("Your character will be a " + raceChoice + " then? (Y/N): ").strip().lower()

          if choice == "y": # if they specify "y" or "Y" for yes then we will return the race they picked as a string. Otherwise we assume they want to pick their race again.
            return raceChoice
        else: # The user typed something numeric that was not a valid race option number
          print(f"'{choice}' is not a valid row number. Try again")
      except: # error was caught in try clause when the user's choice could not be converted to integer
        if choice != "info" and choice != "random": # in case the user chose info or random, we will not alert them to anything. Loop will just repeat with no prompt
          print(f"I'm sorry, I didn't understand '{choice}' ") # Inform the user of their mistake and let them try again.

# The user will select a Dungeons & Dragons character race using the pickRace() function above
raceChoice = pickRace()
print()


# ---------------------------------- CHARACTER CLASS I/O ----------------------------------

def pickClass():
  '''
  EFFECTS: Allows the user to select a class option for their character (returns class choice as string). Additionally if the user would like to know more 
  about a particular class, a webpage will open up on their default browser displaying more information about the class.

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Print out all possible class options to user and let user know they can select a class randomly, or they can find out more about a particular class
    - Validate user input using while loop and input if/elif/else checks
        - If the user chose to find out more about a class then...
            - Use another while loop to validate input on which class they would like to know more about
                - open up web page in their default browser on the class they wanted to know more about
                - if this fails, catch the exception and inform user
        - If the user chose to pick their class randomly, then use random number generator to pick number associated with class option
        - If the user chose to pick a class option, then confirm the user's choice and return string of class that was associated with the number class option the user chose
        - Otherwise if the user made a mistake making a selection, then inform the user and let them try again
  '''

  # list of possible classes avaliable in Dungeons and Dragons 5th edition that the user can pick from
  classes = ["Barbarian","Bard","Cleric","Druid","Fighter","Monk","Paladin","Ranger","Rogue","Sorcerer","Warlock","Wizard"]

  print("Next is your character's class. Choose from among these options:\n")

  # formatting the class options to the user
  # Options will look like "1) Barbarian ", "2) Bard", etc.
  for i in range(0,12):
    print(str(i+1) + ") " + classes[i])

  print()
  print("If you would like to know more about a particular class before you make your choice, type 'info' below.")
  print("If you would like a class picked for you, type 'random' below.")
  print("Otherwise please just type the row number of the class you want your character to have below") 

  # User class option selection and input validation loop
  while True:
      choice = input("\nClass Option: ").strip().lower()

      # Should the user want to know more about a class
      if choice == "info":
        # User class option information selection and input validation loop
        while True:
          choice = input("\nWhich of the classes would you like to know more about? \n(type a row number or 'none' to go back): ").strip().lower()
          if choice == 'none': # The user is done wanting more information and will return back to the class option selection loop
            break 
          try: # if the user enters in something that is not a numeric value, the outer except clause will trigger
            if int(choice) > 0 and int(choice) < 13: # the user can only pick among the 12 classes available
              
              classStr = classes[int(choice)-1].lower()# save the class the user picked as a string
              print("\nOpening:  https://www.dndbeyond.com/classes/" + classStr + "\n")
              try:
                # Open webpage associated with the class the user wants to know more about
                wb.open('https://www.dndbeyond.com/classes/' + classStr)
              except: # If for some reason the application fails to open the browser to the right page 
                print("Sorry, unable to open URL in browser.")
              break # return to class option selection loop
            else: # The user selected a numeric value that was not a valid option. Inform user and let them try again
              print(f"'{choice}' is not a valid row number. Try again")
              print()
          except: # The user typed a non numeric value that caused an exception when attempting to convert to an integer.  Inform user and let them try again
            print(f"I'm sorry, I didn't understand '{choice}' ")
            continue
        
        continue # Go back to character class prompt

      # Pick a class at random for the user
      elif choice == "random":
        # if the user wanted their character's class selected randomly, then assign a class option number randomly
        choice = random.randrange(1,13) # randrange returns integer between inclusive lower bound and exclusive upper bound

      try:# if the user enters in something that is not a numeric value, the except clause will trigger
        if int(choice) > 0 and int(choice) < 13: # the user can only pick among the twelve classes available
          classChoice = classes[int(choice)-1] # save the class the user picked as a string

          # Confirm that user is okay with the class option they selected
          choice = input("Your character will be a " + classChoice + " then? (Y/N): ").strip().lower()

          if choice == "y":  # if they specify "y" or "Y" for yes then we will return the class they picked as a string. Otherwise we assume they want to pick their race again.
            return classChoice

        else: # The user typed something numeric that was not a valid class option number
          print(f"'{choice}' is not a valid row number. Try again")
          print()
      except: # error was caught in try clause when the user's choice could not be converted to integer
        if choice != "info" and choice != "random": # in case the user chose info or random, we will not alert them to anything. Loop will just repeat with no prompt
          print("I'm sorry, I didn't understand.") # Inform the user of their mistake and let them try again.

# The user will select a Dungeons & Dragons character class using the pickClass() function above
classChoice = pickClass()
print()


# ---------------------------------- ABILITY SCORE CALCULATIONS ----------------------------------


print("Now it's time to calculate ability score values! 6 values will be displayed down below.")
print("You will be asked which values will go to which of your character's ability score. \n")

def rollScores():
  '''
  EFECTS: Returns list of six ability scores values that were calculated according to Dungeons & Dragons rules.

  HELPS: Main()

  IMPLEMENTATION SKETCH: 
    - In order to simulate the same probability as rolling a real dice for ability scores, we will follow the same strategy:
        - For each ability score, we roll a six-sided dice four times.
        - We take the sum of the highest three rolls and that becomes an ability score value that gets appended to a values list
        - We do this process a total of six times for each ability score
    - We then return the list of ability score integer values.
  '''

  # list where each ability score value is kept
  values = []
  
  for score in range(1,7): # For each of the six ability scores... (Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma)
    rolls = [] # where each roll of a six-sided dice gets stored

    for roll in range(1,5): # ... we roll 4 dice...
      rolls.append(random.randrange(1,7)) # ... And add each roll to the rolls list
    
    # We then sort the rolls in ascending order
    rolls.sort()

    sum = 0 # this sum will add up each of the...
    for i in range(1,4): # ... three highest rolls (i.e. rolls[1], rolls[2], and rolls[3])
      sum += rolls[i]
    
    # We then add this sum as a potential score to value list
    values.append(sum)

  # Finally we will have a score for each of the six ability scores and we return this list
  return values


# We roll our six ability score values and let the user decide if they want to reroll their scores or proceed
while True:

  # Obtain a list of potential ability scores
  Scores = rollScores()


  for score in range(0,6): # For each of the six ability scores... (Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma)
    print(f"{score+1}) {Scores[score]}") # Print out a score value that was rolled, in the format of "1) 16", "2) 7", etc.
  print()

  # Prompt the user to confirm if they would like to keep their scores or re-roll them
  choice = input("Would you like to re-roll your ability scores? (Y/N): ").strip().lower()

  # if the user is happy with their roles (meaning they typed "n" or "N"), then let them proceed. Otherwise re-roll the scores.
  if choice == "n": 
    break
print()


def assignScores(Scores):
  '''
  EFFECTS: Allows the user to assign ability score values based on a list of ability score dice rolls (the argument 'Scores')

  REQUIRES: Scores must contain six integer values

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Create a dictionary mapping each ability score to its value (which starts off as None)
    - Create a used scores list that shows the user which score values they have already used
    - For each of the ability scores (keys in the dictionary)....
        - Let the user assign an ability score a value they rolled in the Scores list
        - Do not let the user use the same score value more than once and validate
        - Should the user type an invalid input, inform them and let them try again
    - Once each ability score has been mapped to a unique score value, return the ability scores dictionary
  '''

  # Dictionary of all ability scores avaliable in Dungeons and Dragons 5th edition that a character has.
  # Each ability will be mapped to an integer representing the ability score value
  abScores = {"Strength" : None, "Dexterity" : None, "Constitution" : None, "Intelligence" : None, "Wisdom" : None, "Charisma" : None}

  # This list will keep track of which ability score choicrs have already been allocated a value 
  # (Starts empty as the user has not selected any yet)
  usedScores = []

  # For each of the six abilities (the keys of the abScores dictionary)...
  for ab in abScores.keys():

    # User score selection and input validation loop
    while True: 
      print(f"Rows who's values have already been used: {usedScores}") # display which score options from the previous listing have already been allocated

      # Prompt user to allocate a score for a particular ability
      choice = input(f"Which score would you like to go in {ab}? (select the row number): ").strip().lower()

      try: # if the user types a non numeric value, then an exception will be thrown, triggering the except clause

        if choice in usedScores: # the user cannot allocate more than one value to a single ability. Inform them and let them try again
          print(f"you already used the score for row {choice}")
          print()
        elif int(choice) > 0 and int(choice) < 7: # The user can only pick among the 6 cores rolled prior 
          abScores[ab] = Scores[int(choice)-1] # Map a specific ability to a specific score that has been selected by the user
          usedScores.append(choice) # Mark off one of the scores as being used by appending the row choice to the usedScores list
          print()
          break # return back to while loop to continue allocating ability scores
        else: # The user typed in a numeric, but non valid option. Inform the user and try again
          print(f"'{choice}' is not a valid row number. Try again")
          print()
      except: # The user typed a non numeric option when picking an ability score option. Inform the user and try again
        print(f"'{choice}' is not a valid row number. Try again!") 
        print()

  return abScores # Return dictionary mapping of abilities to score values


# Allow the user assign their ability score rolls and reroll if they are not satisfied
while True:
  abScores = assignScores(Scores) # Obtain ability score dictionary from scores rolled after user has allocated each score accordingly
  print(f"Your character has the following ability scores: \n{abScores}")
  print()
  print("Are you satisfied with your ability scores?")

  # Allow the user one last chance to confirm whether or not they want to keep their ability scores mapped as they currently are or reallocate their ability score values
  choice = input("( 'Y' to move on / 'N' to reallocate scores): ").strip().lower()

  # If the user types yes ("y" or "Y") then we proceed with character creation. Otherwise we re-print the scores rolled and allow the user to reallocate them once again. 
  if choice == "y":
    break
  else:
      print()
      for score in range(0,6): # For each of the six ability scores... (Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma)
        print(f"{score+1}) {Scores[score]}") # Print out a score value that was rolled, in the format of "1) 16", "2) 7", etc.
      print()


# ---------------------------------- NAME, GENDER, AND AGE ASSIGNMENT ----------------------------------

def genderAssignment():
  '''
  EFFECTS: Allows the user to select a gender option for their character

  HELPS: Main()

  IMPLEMENTATION SKETCH: 
    - Use while loop to validate user input with if/elif/else checks
        - Assign the user's gender choice with the option they picked
        - If the user typed something invalid as input, inform them and let them try again
    - Return the user's gender option (as string)
  '''

  print("\nWhat is your character's gender? \n")

  # User gender option selection and input validation loop
  while True:
    print("1) Woman \n2) Man \n3) Ambiguous \n")  # Print out all of the options
    choice = input("Gender Option (please select row number): ").strip().lower() # Take in user input (guide them to type number)
    
    # set the user's gender option as a string, otherwise prompt the user to try again
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

  return genderChoice # return user's gender option


# User gender selection and input loop (simplified to only proceed on a yes condition)
while True:
  genderChoice = genderAssignment()
  choice = input(f"You went with the gender option: {genderChoice} \nIs this correct (Y/N): ").strip().lower()
  if choice == "y":
    break



def ageAssignment():
  '''
  EFFETCS: Allows the user to pick an age for their character and also provides information (obtained through webscrapping) 
  on race specific age-ranges based on what the user had previously selected as their character's race.

  HELPS: Main()

  IMPLEMENTATION SKETCH: 
    - Attempt to webscrape data from web page containing information about a character's race
        - Create webscrapping parser so that we can retrieve exact age/lifespan information about character's race
        - Decide on parsing parameter using user's character race option
        - Print age/lifespan information about character race to user
    - If the webscrapping/parsing fails, then inform the user and move on to age selection
    - Use while loop to validate user age input with if/elif/else checks
        - Assign the user's age choice with the option they picked
        - If the user typed something invalid as input, inform them and let them try again
    - Return the user's age option (as string)
  '''

  print("\nHow old is your character?")
  print(f"In case you were wondering, here is some information about the lifespan of the {raceChoice} race:\n")

  try:
    # Attempt to obtain data scrapped from website (data correlating to information about the user's selected race)
    # raceChoice has global scope so there is no need to pass it to function as argument
    res = requests.get('http://dnd5e.wikidot.com/' + raceChoice.lower())

    # In the event gathering the webscrapped data failed, an exception is raised
    res.raise_for_status()

    # We create a parser for the webscrapped data
    AgeSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    # We need to select some parameters specific to parsing the data obtained for a specfic race 
    if raceChoice == 'Human' or raceChoice == 'Dragonborn':
      childNum = '1'
    elif raceChoice == 'Elf' or raceChoice == "Tiefling":
      childNum = '5'
    elif raceChoice == 'Half-Elf' or raceChoice == 'Half-Orc':
      childNum = '3'
    else:
      childNum = '2'

    # This parses/obtains the specific string containing information about a particular race's longevity and how long they live on average from the webscrapped page html data.
    elems = AgeSoup.select('#page-content > div.feature > div:nth-child(1) > div > ul:nth-child(' + childNum + ') > li')
    print('"' + elems[0].getText() + '"') # We present this information to the user so they can be informed before making a decision on their character's age
  except: # An exception was thrown when attempting to webscrape data
      print("Sorry, couldn't obtain information. You may want to check your internet connection.")

  # User age selection and input validation loop
  while True:
    ageChoice = input("\nHow old would you like your character to be? (please enter a number of years): ").strip()
    try:
      if int(ageChoice) >= 0 and int(ageChoice) < 100000000: # If the user enters a valid age, then we return the age selected as a string
        return ageChoice
      else:
        print(f"'{ageChoice}' is an invalid age") # Inform the user they selected an invalid age and let them try again.
    except: # User entered a non numeric value for age, which threw an exception when trying to convert to an integer. Inform the user and let them try again. 
      print("Your age must be in the form of a number like '5' '60' or '374'")


# User age selection and input loop (simplified to only proceed on a yes condition)
while True:
  ageChoice = ageAssignment()
  choice = input(f"So your character is {ageChoice} years old? \nIs this correct (Y/N): ").strip().lower()
  if choice == "y":
    break


# Character name assignment beings here

print("\nNow let's give your character a name!")
print("If you would like, I can help you find some names based on your character's race and gender (just type 'help' below) ")

# Check to see if the user has the DNP_Characters directory where the character shelve should be
try:
  shelfFile = shelve.open('.\DNP_Characters\Characters') # if so we open the character shelve file
except: 
  os.mkdir('DNP_Characters') # in the event the user does not yet have a DNP_Characters folder, we make one for them an open a character shelve file
  shelfFile = shelve.open('.\DNP_Characters\Characters')

# We open the shelve here to make sure that when we call nameAssignment(), we do not let the user name the character a name
# that is the same as an existing character. The keys in a shelve (which basically functions the same as a vanilla python dictionary) are character names 
# which must be unique. We will check that this uniqueness is preserved in nameAssignment()'s function definition. 

def nameAssignment():
  '''
  EFFECTS: Collects character name information from the user and ensures that it does not match an existing character's name.
  We will also supply the user with the option to learn more about common names given their prior race selection.  
  NOTE: the shelve object `shelfFile` and race selection `raceChoice` both have global scope when defined above and do not need to be passed as arguments.

  HELPS: Main()

  IMPLEMENTATION SKETCH:
    - Use while loop to validate user name input with if/elif/else checks
        - If the user typed something invalid as input (name being blank or another character in shelve already sharing the same name), inform them and let them try again.
        - If the user wanted help, then open a webpage in the user's default browser corresponding to the user's race selection and common names thereof
            - If opening the browser/webpage fails we inform the user and move on
        - Otherwise assign the user's name choice with the option they picked
    - Return the user's name option (as string)

  '''

  # User name selection and input validation loop
  while True:
    nameChoice = input("Name Option: ").strip()
    if nameChoice == '': # character name cannot be blank string. Inform the user and let them try again. 
      print("\nYou must give your character a name!\n")
    elif nameChoice in shelfFile.keys(): # do not allow user to name character if there exists a character with the same name already. Inform the user and let them try again. 
      print(f"\nYou already have a character called {nameChoice}. You must use a new name!\n")
    elif nameChoice.lower() == 'help':

      # Open a web page corresponding to the user's race selection and common names thereof
      print("\nOpening:  https://www.fantasynamegenerators.com/dnd-" + raceChoice.lower() + "-names.php" + "\n") # https://www.fantasynamegenerators.com/dnd-dragonborn-names.php
      try:
        wb.open("https://www.fantasynamegenerators.com/dnd-" + raceChoice.lower() + "-names.php")
      except: # In the event opening the web page fails and throws an exception, we catch the exception and inform the user.
        print("Sorry, unable to open URL in browser.\n")
      
    elif len(nameChoice) > 40: # Name choice should not be longer than 40 characters.
      print("\nName must be less than 40 letters\n")

    else: # If the name passes all the previous checks then we return the selection as a string
      return nameChoice


# User name selection and input loop (simplified to only proceed on a yes condition)
while True:
  nameChoice = nameAssignment()
  choice = input(f"Your character's name is {nameChoice}? (Y/N): ").strip().lower()
  if choice == "y":
    break



# ---------------------------------- CHARACTER FINALIZATION ----------------------------------

print()
helpHeader(40,"Character Finalization") # display the character finalization header

# Present the user all of their choices made thus far and present them with editing options
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

  # Give the user the chance one last time to change anything they want about their character, or if they are finished, save their character to the shelve and end the application.
  choice = input("Finalization Option: ").strip().lower() 
  if choice == "y":
    # Create the actual character object using the user's choices as constructor arguments 
    NewChar = Character(raceChoice, classChoice, nameChoice, ageChoice, genderChoice, abScores)
    
    # Save the final character object to the shelve so that it exists across multiple sessions of the app and close the shelve file
    shelfFile[nameChoice] = NewChar
    shelfFile.close()

    print(f"{nameChoice} is now an established character! \nTo manage {nameChoice}'s information, restart DungeonsNPythons and select the manage existing character option!\nAll characters are stored in a folder called 'DNP_Characters' so do NOT delete that folder unless you want to lose all your characters!\n\n")
    break # This will break out of the final input loop and end the application.

  # Options for the user to edit any decision made thus far 
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
  elif choice == "6": # Re-rolling and reallocating ability scores requires a bit of set up. Namely displaying each score rolled and letting the user re-roll if they want to.
    
    # re-roll ability score values
    while True:
      Scores = rollScores()

      # Display each score rolled
      for score in range(0,6):
        print(f"{score+1}) {Scores[score]}")
      print()

      # Allow the user to re-roll scores if they would like
      choice = input("Would you like to re-roll your ability scores? (Y/N): ").strip().lower()
      if choice == "n":
        break
    print()

    # Let the user reallocate ability score values
    abScores = assignScores(Scores)

  else: # If the user types something not among the listed options. We inform the user and let them try again.
    print(f"I'm sorry, I didn't understand '{choice}' \n")


# NOTE: program will terminate after a new character is created.        
