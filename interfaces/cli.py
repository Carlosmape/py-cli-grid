import os
import time

from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.frame import Frame
from engine.interface import GUI
from engine.items.interactives.containeritem import container_item
from engine.items.interactives.WearableItem import WearableItem
from engine.world.area_types import area_types

from .colors import style
from .KBHit import KBHit

keyboard = KBHit()

# System call
os.system("")

##########
# CLI Interface
##########
class CommandLineInterface(GUI):
    # Ascii icons
    strPlayer =  '#'
    strItem = '\''
    strWearable = 'ª'
    strContainer = 'º'
    strNPC = 'Ö'
    strNPC1 = 'Ô'
    strNPC2 = 'Ò'
    strNPC3 = 'Ó'
    strDoor = '░'
    strEmptyBar = '▒'
    strWall = '█'
    strTopLimit = '▄'
    strBotLimit = '▀'
    strNone = ' '
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
        self.max_frame_rate = 24
        self.show_action_menu = False
        self.mesg_showed_times = 0
        # Get shell size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines


    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        elif keyboard.kbhit():
            return keyboard.getch()

    def doAction(self, action: bytes, player: PlayerCharacter):
        if action == ('w' or 'W'):
            player.move_north(self.last_frame.area)
        elif action == ('a' or 'A'):
            player.move_west(self.last_frame.area)
        elif action == ('s' or 'S'):
            player.move_south(self.last_frame.area)
        elif action == ('d' or 'D'):
            player.move_east(self.last_frame.area)
        elif action == (' '):
            self.last_frame.menu = player.active_action_menu(self.last_frame.area)
        elif action == b'\x03':
            exit()

    def clear(self):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')

    def render(self, frame: Frame):
        frame_str = self.__frame_str(frame)
        lines = frame_str.count('\n') + 1
        # Add console size to fit in whole console
        frame_str += "\n" * (self.height - lines)
        print(frame_str, end='\r')

    def manage_exceptions(self, ex: BaseException):

        # Call super method without return to avoid game exit
        super().manage_exceptions(ex)

        # If KeyboardInterrupt do not exit the game
        if isinstance(ex, KeyboardInterrupt):
            return False

        # Show exception info
        else:
            msg = "An error ocurrer during the game\n"
            msg += str(ex.with_traceback()) + "\n"
            msg += "Aborting the game execution"
            input(msg)
            return True

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
        pj_str = str()
        if frame.player:
            pj = frame.player
            # Name and position
            pj_str += style.CBOLD + ("\n%s (%s)>") % (pj.name, pj.get_level()) + style.CEND
            # Player status
            strXP = self.strWall * pj.stats.experience()
            strXP += self.strEmptyBar * pj.stats.remain_experience()
            pj_str += style.CVIOLET + "\n XP(%s/%s)\t" %(pj.stats.experience(), pj.stats.experience()+pj.stats.remain_experience())
            pj_str += strXP
            strHP = self.strWall * pj.get_health()
            strHP += self.strEmptyBar * (pj.get_max_health() - pj.get_health()) 
            pj_str += style.CRED + "\n HP(%s/%s)\t" %(pj.get_health(), pj.get_max_health())
            pj_str += strHP
            pj_str += style.CYELLOW + "\n Agility:" + str(pj.get_agility())
            pj_str += style.CGREEN + "\n Strength: " + str(pj.get_strength())
            pj_str += style.CBLUE2 + "\n Speed: " + str(round(pj.get_speed(),2)) + style.CEND
            # Player equipment
            pj_str += style.CBOLD + "\nEquipment>" + style.CEND
            pj_str += "\n Head: " + str(pj.items[BodyParts.head] or '-')
            pj_str += "\n Shoulders: " + str(pj.items[BodyParts.shoulder] or '-')
            pj_str += "\n Arms: " + str(pj.items[BodyParts.arms] or '-')
            pj_str += "\n Hands: " + str(pj.items[BodyParts.hands] or '-')
            pj_str += "\n Chest: " + str(pj.items[BodyParts.chest] or '-')
            pj_str += "\n Back: " + str(pj.items[BodyParts.back] or '-')
            pj_str += "\n Core: " + str(pj.items[BodyParts.core] or '-')
            pj_str += "\n Legs: " + str(pj.items[BodyParts.legs] or '-')
            pj_str += "\n Feets: " + str(pj.items[BodyParts.feets] or '-')
            pj_str += style.CEND
            # Quests
            if pj.quests:
                pj_str += "\n" + style.CBOLD + "Quest>" + style.CEND
                for q in pj.quests:
                    if not q.objective.done:
                        pj_str += "\n " + q.name 
                        pj_str += " "
                        pj_str += q.description
        return pj_str

    def __area_str(self, frame: Frame):
        frame_str = str()
        if frame.area:
            # Print area type
            frame_str += style.CBOLD + "Area: " + area_types.NAMES[frame.area.type] + ">" + style.CEND
            # Its needed to draw inverted due to console works from top to down
            frame_str += style.CBLACK
            frame_str += "\n" + (self.strTopLimit* (3+frame.area.width)) + "\n"
            for y in range(frame.area.height, -1, -1):
                frame_str += style.CBEIGEBG + style.CBLACK + self.strWall
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
                        frame_str += self.strNone
                frame_str += self.strWall + style.CEND + "\n"
            frame_str += style.CBLACKBG + style.CBLACK + self.strBotLimit * (3+frame.area.width) + style.CEND

        return frame_str

    def __menu_str(self, frame: Frame):
        frame_str = str()
        if frame.menu:
            frame_str += style.CBOLD + "\n-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    frame_str += " (%s)%s" % (frame.menu.options.index(option), option)
            frame_str += "\n" + frame.menu.query + style.CEND

        return frame_str

    def __message_str(self, frame: Frame):
        frame_str = str()
        # Log messages
        if len(frame.get_msg()) > 0:
            frame_str += "\n"+ style.CBOLD + "Log> "
            for msg in frame.get_msg():
                frame_str += "\n " + msg
        return frame_str + style.CEND
