# Loose load function implementation
import csv
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

#Global variables
TXT_HEIGHT   = 1
TXT_WIDTH    = 37
VERT_PAD     = 10
BORDER       = 5
BUTTON_SPACE = 5
SORTING      = ""

TYPE_LIST = ["Creature", "Artifact", "Enchantment", "Instant", "Sorcery", "Land", "Planeswalker", "Battle", "Tribal"]
COLORS    = ["U", "W", "B", "R", "G"]

#Creates the way we will classify cards
class Card :

    name   = ""
    type   = ""
    color  = ""
    rarity = ""
    
    cost   = ""

    def __init__ (self, name, type, color, rarity, cost):
        self.name   = name
        self.type   = type
        self.color  = color
        self.rarity = rarity
        self.cost   = cost

#Chooses the deck file
def chooseFile():
    filetypes = [("deck files", "*.csv")]
    

    fileName = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    deckFileTextBox.delete("1.0","end")
    deckFileTextBox.insert(tk.END, fileName)

#Loads the deck
def loadUserDeck():

    deckFile = deckFileTextBox.get("1.0",tk.END)
    deckFile = deckFile[:-1]

    with open(deckFile, newline='') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        masterNames = []

        for card in masterDeck:
            masterNames.append(card.name)

        # Clear the user list before adding more cards
        userDeckListBox.delete(0,tk.END)
        
        try:
            for row in reader:
                # Pass relevant card parameters to Card constructor and add to list
                newcard = Card(row["name"], row["type"], row["colorIdentity"], row["rarity"], row["manaValue"])

                # Check to see if the card is in the master deck
                if newcard.name in masterNames:
                    userDeck.append(newcard)
                    userDeckListBox.insert(tk.END,newcard.name)
                else:
                    print(f'\nInvalid card: {newcard.name}')

        except:
            pass

#Loads the list of all cards
def loadMasterDeck():
    masterDeckFile = "./cards.csv"

    with open(masterDeckFile, newline='') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        try:
            for row in reader:
                # Pass relevant card parameters to Card constructor and add to list
                newcard = Card(row["name"], row["type"], row["colorIdentity"], row["rarity"], row["manaValue"])

                masterDeck.append(newcard)

        except:
            pass

#Sorts the cards    
def sort(event):

    if len(userDeck) == 0:
        return
    
    # Clear the sorted list before adding more cards
    sortedDeckListBox.delete(0,tk.END)

    # Grab combobox values
    whichOne = sortTypeComboBox.get()
    option   = sortedComboBox.get()

    # Sort by type
    if whichOne == "Type":
        sortedComboBox["values"] = TYPE_LIST

        resultList = []

        for card in userDeck:
            if option.lower() in card.type.lower():
                if card.name not in resultList:
                    resultList.append(card.name)
                    sortedDeckListBox.insert(tk.END,card.name)

    # Sort by mana value
    elif whichOne == "Mana Cost":

        manaValueList = []

        for card in userDeck:
            if option in card.cost:
                if card.name not in manaValueList:
                    manaValueList.append(card.name)
                    sortedDeckListBox.insert(tk.END,card.name)

    # Sort by Color
    elif whichOne == "Color":

        colorIdentityList = []

        for card in userDeck:
            if option in card.color:
                if card.name not in colorIdentityList:
                    if (option == "") and (card.color not in COLORS):
                        colorIdentityList.append(card.name)
                        sortedDeckListBox.insert(tk.END,card.name)
                    if option != "":
                        colorIdentityList.append(card.name)
                        sortedDeckListBox.insert(tk.END,card.name)


    # Sort by Rarity
    elif whichOne == "Rarity":

        rarityList = []

        for card in userDeck:
            if option in card.rarity:
                if card.name not in rarityList:
                    if option == "common" and "un" not in card.rarity:
                        rarityList.append(card.name)
                        sortedDeckListBox.insert(tk.END,card.name)
                    
                    if option != "common":
                        rarityList.append(card.name)
                        sortedDeckListBox.insert(tk.END,card.name)      

    else:
        pass

def sortCheck(event):

    if len(userDeck) == 0:
        return

    whichOne = sortTypeComboBox.get()    

    if whichOne == "Type":
        sortedComboBox["values"] = TYPE_LIST

    elif whichOne == "Mana Cost":

        manaValueList = []

        for card in userDeck:
            if card.cost not in manaValueList:
                manaValueList.append(card.cost)
                sortedComboBox["values"] = manaValueList

    elif whichOne == "Color":

        colorIdentityList = []
        
        for card in userDeck:
            if card.color not in colorIdentityList:
                colorIdentityList.append(card.color)
                sortedComboBox["values"] = colorIdentityList

    elif whichOne == "Rarity":

        rarityList = []

        for card in userDeck:
            if card.rarity not in rarityList:
                rarityList.append(card.rarity)
                sortedComboBox["values"] = rarityList

    else:
        pass

def closeProgram():
    exit()


if __name__ == '__main__':

    # Main gui variable
    gui = tk.Tk()
    gui.title("Magic the Gathering Card Sorter")

    # Deck related variables
    fileName   = ""
    masterDeck = []
    userDeck   = []
    filterDeck = []

    # GUI Objects
    topPane           = tk.PanedWindow(gui)
    deckFileTextBox   = tk.Text(gui, height=TXT_HEIGHT, width=TXT_WIDTH, bd=BORDER)
    deckFileLabel     = tk.Label(gui, text="Deck File: ")
    userDeckLabel     = tk.Label(gui, text="Deck")
    sortedLabel       = tk.Label(gui, text="Filtered Cards")
    fileChooseButton  = tk.Button(gui, height=1, width=10, text = "Choose Deck", command = chooseFile)
    loadCardsButton   = tk.Button(gui, height=1, width=10, text = "Load Deck", command = loadUserDeck)
    exitButton        = tk.Button(gui, height=1, width=10, text = "Exit", command = closeProgram)
    userDeckListBox   = tk.Listbox(gui, height=20, width=50, bd=BORDER)
    sortedDeckListBox = tk.Listbox(gui, height=20, width=50, bd=BORDER)
    sortTypeComboBox  = ttk.Combobox(gui, width=48, values=["Type", "Color", "Rarity", "Mana Cost"])
    sortedComboBox    = ttk.Combobox(gui, width=48)
    image             = tk.PhotoImage(file="./colorwheel.png")
    mtgimage          = tk.PhotoImage(file="./mtglogo.png")
    colorWheel        = tk.Label(gui, image=image)
    mtgLogo           = tk.Label(gui, image=mtgimage)

    # Add Objects to appropriate pane
    topPane.add(deckFileTextBox)
    topPane.add(fileChooseButton)
    topPane.add(loadCardsButton)
    topPane.add(exitButton)
    topPane.add(deckFileLabel)
    topPane.add(userDeckLabel)
    topPane.add(sortedLabel)
    topPane.add(userDeckListBox)
    topPane.add(sortedDeckListBox)
    topPane.add(sortTypeComboBox)
    topPane.add(sortedComboBox)
    topPane.add(colorWheel)
    topPane.add(mtgLogo)

    # Position objects using .grid method
    deckFileLabel   .grid(column = 0, row = 0, pady = VERT_PAD)
    userDeckLabel   .grid(column = 1, row = 2, pady = VERT_PAD)
    sortedLabel     .grid(column = 2, row = 2, pady = VERT_PAD)

    deckFileTextBox .grid(column = 1, row = 0, pady = VERT_PAD, sticky="W")

    fileChooseButton.grid(column = 0, row = 1, pady = VERT_PAD, padx=BUTTON_SPACE)
    loadCardsButton .grid(column = 0, row = 2, sticky = "NW", pady = VERT_PAD, padx=BUTTON_SPACE)
    exitButton      .grid(column = 0, row = 4, sticky = "NW", pady = VERT_PAD, padx=BUTTON_SPACE)

    sortedDeckListBox.grid(column = 2, row = 3, sticky = "W", padx=BUTTON_SPACE, pady=BUTTON_SPACE)
    userDeckListBox  .grid(column = 1, row = 3, sticky = "W", pady=BUTTON_SPACE)

    sortTypeComboBox.grid(column = 1, row = 1, sticky="W")
    sortedComboBox  .grid(column = 2, row = 1, sticky="W", padx=BUTTON_SPACE)

    colorWheel    .grid(column = 0, row = 3, sticky="N")
    mtgLogo       .grid(column = 2, row = 0, sticky="N")

    # Bind combobox methods
    sortTypeComboBox.bind("<<ComboboxSelected>>", sortCheck)
    sortedComboBox  .bind("<<ComboboxSelected>>", sort)

    # Position panes
    topPane.   grid(column = 0, row = 0)

    # Load the master deck
    loadMasterDeck()

    # Display GUI
    gui.mainloop()