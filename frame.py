from room import *
from charachter import * 

##########
# Menu class
# Struct to manage menus to be rendered
##########
class Menu():
    def __init__(self, title, query, options=None):
        self.title = title
        self.options = options
        self.query = query

    def isValidOption(self, givenOption):
        if self.options:
            if givenOption.isnumeric():
                return 0 <= int(givenOption) < len(self.options)
            else:
                return False
        elif type(givenOption) is str:
            return True
        else:
            return False

class MenuLoadGame():
    def __init__(self, title, query, options):
        super().__init__(title, query, options):

##########
# Frame class
# Contains data to be rendered (Menu, Player, Room and information Messages)
##########
class Frame():
    msgQueue = list("")
    def __init__(self, room: Room, player: PlayerCharachter, menu: Menu = None):
        self.room = room
        self.player = player
        self.menu = menu

    def addMessage(self, msg: str):
        self.msgQueue.append(msg)
