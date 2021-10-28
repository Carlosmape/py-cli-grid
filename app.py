import os

from defines import *
from items import *
from charachter import *
from room import *
from interface import *

STORE_PATH = str("saves/")

class App():
    def __init__(self, interface):
        self.interface = interface
        iSelectedGame = self.checkSavedGames()
        if iSelectedGame == 0:
            self.initializeGame()
        else:
            self.loadGame(iSelectedGame)

    def checkSavedGames(self):
        if os.listdir(STORE_PATH) != []:
            #Compose the menu
            strMenu = str("\nSelect a option to start playing ...\n")
            lOptions=["New Adventure!"]
            lOptions += os.listdir("saves/")
            menu = Menu("Do you want to continue last adventures?", "Select a option:", lOptions)
            iSelectedGame = self.interface.displayMenu(menu)
        else:
            iSelectedGame = 0;
        return int(iSelectedGame)

    def initializeGame(self):
        menu = Menu("You are about to start a new adventure...", "Tell me your name, brave")
        strPlayerName = self.interface.displayMenu(menu)
        menu = Menu("You wake up in a dark room... %s"%(strPlayerName), "Let's look for the way to leave this place!")
        self.interface.displayMenu(menu)
        # Initialize world and player
        self.Room = Room(True)
        self.Player = PlayerCharachter(strPlayerName)
    
    def loadGame(self, savedGame):
        #TODO is doing the same as InitializeGame
        self.Room = Room()
        self.Player = PlayerCharachter()
    
    def run(self):
        end=False
        while end == False:
            # TODO: add here foe's IA
            # self.Room.
            frame = Frame(self.Room, self.Player)
            self.interface.displayFrame(frame)

            #action = input()
            #if action == "exit":
            #    end = True

        self.interface.displayMessage("Game stopped")
        

