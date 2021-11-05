import os
import sys

try:
    from msvcrt import getch
except ImportError:
    from readchar import readchar

from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines import Position
from engine.frame import Frame
from engine.interface import Interface


###
class keyboard():
    @staticmethod
    def read():
        if os.name in ('nt', 'dos'):
            return getch()
        else:
            return bytes(readchar(), sys.getfilesystemencoding())
##########
# CLI Interface
##########
class CommandLineInterface(Interface):
    # Ascii icons
    strPlayer = '#'
    strItem = 'º'
    strNPC = 'O'
    strDoor = '▲'
    strWall = '█'
    strTopLimit = '▄'
    strBotLimit = '▀'

    # Constructor
    def __init__(self):
        print("Welcome to your CLI Adventure")
        print("Initializing interface")
        super().__init__()
        self.maxFrameRate=5
        self.show_action_menu = False
        #Get shell size
        size=os.get_terminal_size()
        self.width=size.columns
        self.height=size.lines
   
    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        else:
            return keyboard.read()

    def doAction(self, action: bytes, player: PlayerCharacter):
        if action == (b'w' or b'W'):
            player.move_north(self.last_frame.room)
        elif action == (b'a' or b'A'):
            player.move_west(self.last_frame.room)
        elif action == (b's' or b'S'):
            player.move_south(self.last_frame.room)
        elif action == (b'd' or b'D'):
            player.move_east(self.last_frame.room)
        elif action == (b' '):
            print("Action button pushed")
        elif action == b'\x03':
            exit()

    def render(self, frame: Frame):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')
        print(self.__frame_str(frame))

    def __frame_str(self, frame: Frame):
        frame_str = str()
        # Display PJ information
        frame_str += self.__player_str(frame)
        # Render roomw
        frame_str += self.__room_str(frame)
        # Render Menu
        frame_str += self.__menu_str(frame)
        # Render queued messages
        frame_str += self.__message_str(frame)

        return frame_str

    def __player_str(self, frame: Frame):
        frame_str = str()
        if frame.player:
            frame_str += ("%s Position(%s,%s)") % (frame.player.name, frame.player.position.X, frame.player.position.Y)
            frame_str += ("\n\t♥: %s Agility: %s") % (frame.player.health, frame.player.agility)
        return frame_str

    def __room_str(self, frame: Frame):
        frame_str = str()
        if frame.room:
            # Its needed to draw inverted due to console works from top to down
            frame_str += "\n" + (self.strTopLimit* (3+frame.room.width)) + "\n"
            for y in range(frame.room.height, -1, -1):
                frame_str += self.strWall
                for x in range(0, frame.room.width+1, 1):
                    current_position = Position(x,y)
                    if frame.player.position == current_position:
                        frame_str += self.strPlayer
                    elif frame.get_npc(current_position):
                        frame_str += self.strNPC
                    elif current_position in frame.room.doors:
                        frame_str += self.strDoor
                    elif current_position in frame.room.items:
                        frame_str += self.strItem
                    elif current_position in frame.room.walls:
                        frame_str += self.strWall
                    else:
                        frame_str += ' '

                frame_str += self.strWall + "\n"
            frame_str += self.strBotLimit * (3+frame.room.width)

            frame_str += "\n NPCs (%s): " % len(frame.npcs)
            for npc in frame.npcs: frame_str += " (%s,%s)" % (npc.position.X, npc.position.Y)

        return frame_str

    def __menu_str(self, frame: Frame):
        frame_str = str()
        if frame.menu:
            frame_str += "-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    frame_str += "\n %s - %s" % (frame.menu.options.index(option), option)
            frame_str += "\n" + frame.menu.query

        return frame_str

    def __message_str(self, frame: Frame):
        frame_str = str()
        if frame.msgQueue:
            frame_str += "\nWORLD: " + frame.msgQueue.pop()

        return frame_str
