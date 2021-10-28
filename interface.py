import time
import os

from defines import *
from items import *
from charachter import *
from room import *
from frame import *

###########
# Base Interface class 
# (should not be instantiated, should be used as base class and use child instances)
###########
class Interface():
    def __init__(self):
        #Defines frame interval in seconds
        self.maxFrameRate = 25
        self.lastUpdate=time.time()

    # Public method to Display a Frame. 
    def displayFrame(self, frame: Frame): 
        self.__tryRender(frame)

    # Public method to Display a Menu (without Frame)
    def displayMenu(self, menu: Menu):
        self.render(menu)
    
    # Public method to get user input (must be overrided)
    def readUserInput(self):
        raise NotImplementedError()

    # Render a frame within maxframerate
    def __tryRender(self, frame: Frame):
        if time.time() - self.lastUpdate > 1/self.maxFrameRate:
            self.lastUpdate = time.time()
            self.render(frame)

    # Render a frame without maxframerate 
    def render(self, frame: Frame):
        raise NotImplementedError()

##########
# CLI Interface
##########
class CommandLineInterface(Interface):
    # Ascii icons
    strVWall = '|'
    strHWall = '-'
    strPlayer = '#'
    strItem = '·'
    strNPC = 'O'
    strDoor = '*'
    #
    def __init__(self):
        print("Welcome to your CLI Adventure")
        print("Initializing interface")
        super().__init__()
        self.maxFrameRate=2
    
    def render(self, frame: Frame):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')
        
        print(self.convertToString(frame))

    def displayMenu(self, menu: Menu):
        bSelectedOption = False
        while bSelectedOption == False:
            self.render(Frame(None, None, menu))
            sOption = input()
            bSelectedOption = menu.isValidOption(sOption)
                
        return sOption

    def convertToString(self, frame: Frame):
        stringFrame = str()
        #Display PJ information
        if frame.player:
            stringFrame += ("%s - Health: %s\n") % (frame.player.name, frame.player.health)
        #Render room
        if frame.room:
            stringFrame += "\n"
            stringFrame += "-" * (frame.room.width + 2)
            for i in range(0, frame.room.height):
                stringFrame += "\n"+self.strVWall
                for j in range(0, frame.room.width):
                    if frame.player.position == Position(i,j):
                        stringFrame += self.strPlayer
                    else:
                        stringFrame += ' '
                stringFrame += self.strVWall
            stringFrame += "\n" + "-" * (frame.room.width + 2)
        #Render Menu
        if frame.menu:
            stringFrame += "-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    stringFrame += "\n %s - %s" % (frame.menu.options.index(option), option)
            stringFrame += "\n" + frame.menu.query
        #Render queued messages
        if frame.msgQueue:
            stringFrame += "\nWORLD: " + msgQueue.pop()
        return stringFrame
