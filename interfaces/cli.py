import os
import sys
import time

from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.frame import Frame
from engine.interface import Interface
from engine.items.interactives.containeritem import container_item
from engine.items.interactives.WearableItem import WearableItem
from engine.world.area_types import area_types

try:
    from msvcrt import getch
except ImportError:
    from readchar import readchar

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
    strItem = '\''
    strWearable = 'ª'
    strContainer = 'º'
    strNPC = 'Ö'
    strNPC1 = 'Ô'
    strNPC2 = 'Ò'
    strNPC3 = 'Ó'
    strDoor = '░'
    strWall = '█'
    strTopLimit = '▄'
    strBotLimit = '▀'
    # stuff
    strManSword =  "\n\                      (T)"
    strManSword += "\n \      O        _  0   | "
    strManSword += "\n  \   ó(w)ò }   / \(Y)==o "
    strManSword += "\n  (D_/ | | \|} { º } |  | "
    strManSword += "\n      .|_|. }   \_/___\ | "
    strManSword += "\n       v v         V V  | "
    strManSword += "\n      _l l_       _| |_ | "

    # Constructor
    def __init__(self):

        self.clear()
        print("Initializing interface")
        print(CommandLineInterface.strManSword)
        print("Welcome to your CLI Adventure")
        time.sleep(0.5)

        super().__init__()
        self.maxFrameRate = 5
        self.show_action_menu = False
        # Get shell size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines


    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        else:
            return keyboard.read()

    def doAction(self, action: bytes, player: PlayerCharacter):
        print("doAction", player.menu, str(action))
        
        if action == (b'w' or b'W'):
            player.move_north(self.last_frame.area)
        elif action == (b'a' or b'A'):
            player.move_west(self.last_frame.area)
        elif action == (b's' or b'S'):
            player.move_south(self.last_frame.area)
        elif action == (b'd' or b'D'):
            player.move_east(self.last_frame.area)
        elif action == (b' '):
            self.last_frame.menu = player.active_action_menu(self.last_frame.area)
        elif action == b'\x03':
            exit()

    def clear(self):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')

    def render(self, frame: Frame):
        self.clear()
        print(self.__frame_str(frame))

    def __frame_str(self, frame: Frame):
        frame_str = str()
        # Render areaw
        frame_str += self.__area_str(frame)       
        # Display PJ information
        frame_str += self.__player_str(frame)
        # Render queued messages
        frame_str += self.__message_str(frame)
        # Render Menu
        frame_str += self.__menu_str(frame)


        return frame_str

    def __player_str(self, frame: Frame):
        frame_str = str()
        if frame.player:
            # Name and position
            frame_str += ("\n%s (%s,%s) lv: %s") % (frame.player.name, frame.player.position.X, frame.player.position.Y, frame.player.level)
            # Player status
            frame_str += ("\n\tHealth: %s Agil: %s Stren: %s ") %\
                    (frame.player.get_health(), frame.player.get_agility(), frame.player.get_strength())
            # Player equipment
            frame_str += "\nEquipment:\n\t"
            frame_str += "Head(%s) "% (frame.player.items[BodyParts.head] or '')
            frame_str += "Shoulders(%s) "% (frame.player.items[BodyParts.shoulder] or '')
            frame_str += "Arms(%s) "% (frame.player.items[BodyParts.arms] or '')
            frame_str += "Chest(%s) "% (frame.player.items[BodyParts.chest] or '')
            frame_str += "Hands(%s) "% (frame.player.items[BodyParts.hands] or '')
            frame_str += "Back(%s) "% (frame.player.items[BodyParts.back] or '')
            frame_str += "Core(%s) "% (frame.player.items[BodyParts.core] or '')
            frame_str += "Legs(%s) "% (frame.player.items[BodyParts.legs] or '')
            frame_str += "Feets(%s) "% (frame.player.items[BodyParts.feets] or '')


        return frame_str

    def __area_str(self, frame: Frame):
        frame_str = str()
        if frame.area:
            # Print area type
            frame_str += "Area: " + area_types.NAMES[frame.area.type]
            # Its needed to draw inverted due to console works from top to down
            frame_str += "\n" + (self.strTopLimit* (3+frame.area.width)) + "\n"
            for y in range(frame.area.height, -1, -1):
                frame_str += self.strWall
                for x in range(0, frame.area.width+1, 1):
                    current_position = Position(x,y)
                    if frame.player.position == current_position:
                        frame_str += self.strPlayer
                    elif frame.get_npc(current_position):
                        frame_str += self.strNPC
                    elif current_position in frame.area.doors:
                        frame_str += self.strDoor
                    elif current_position in frame.area.items:
                        item = frame.area.item(current_position)
                        if isinstance(item, WearableItem):
                            frame_str += self.strWearable
                        elif isinstance(item, container_item):
                            frame_str += self.strContainer
                        else:
                            frame_str += self.strItem
                    elif current_position in frame.area.walls:
                        frame_str += self.strWall
                    else:
                        frame_str += ' '

                frame_str += self.strWall + "\n"
            frame_str += self.strBotLimit * (3+frame.area.width)

            frame_str += "\n NPCs (%s): " % len(frame.npcs)
            for npc in frame.npcs: frame_str += " (%s,%s)" % (npc.position.X, npc.position.Y)

        return frame_str

    def __menu_str(self, frame: Frame):
        frame_str = str()
        if frame.menu:
            frame_str += "\n-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    frame_str += " (%s)%s" % (frame.menu.options.index(option), option)
            frame_str += "\n" + frame.menu.query

        return frame_str

    def __message_str(self, frame: Frame):
        frame_str = str()
        if frame.msgQueue:
            frame_str += "\n " + frame.msgQueue.pop()

        return frame_str
