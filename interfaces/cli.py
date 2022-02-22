import os
import time
from traceback import format_exc

from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.frame import Frame
from engine.interface import GUI
from engine.items.interactives.containeritem import container_item
from engine.items.interactives.WearableItem import WearableItem
from engine.menu import MenuPause
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
    strWearable = 'º'
    strContainer = '¤'
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
    strTittle =  "\n __  __       _             ____       _ "
    strTittle += "\n|  \/  | ___ | |_ ___  _ __|  _ \ ___ | |"
    strTittle += "\n| |\/| |/ _ \| __/ _ \| '__| |_) / _ \| |"
    strTittle += "\n| |  | | (_) | || (_) | |  |  _ < (_) | |"
    strTittle += "\n|_|  |_|\___/ \__\___/|_|  |_| \_\___/|_|"

    strManSword =  "\n\             "
    strManSword += "\n \      O     "
    strManSword += "\n  \   ó(w)ò } "
    strManSword += "\n  (D_/ | | \|}"
    strManSword += "\n      .|_|. } "
    strManSword += "\n       v v    "
    strManSword += "\n      _l l_   "

    strWomanSword =  "\n        (T)"
    strWomanSword += "\n  _  0   | "
    strWomanSword += "\n / \(Y)==o "
    strWomanSword += "\n{ º } |  | "
    strWomanSword += "\n \_/___\ | "
    strWomanSword += "\n    V V  | "
    strWomanSword += "\n   _| |_ | "

    # Constructor
    def __init__(self):

        #Super initialization
        self.clear()
        print(CommandLineInterface.strTittle)
        print("\n\t   Initializing interface")
        print("\n\tWelcome to your CLI Adventure")
        super().__init__()
        time.sleep(1)

        # Own configuration
        self.clear()
        print(CommandLineInterface.strManSword)
        self.max_frame_rate = 24
        self.show_action_menu = False
        self.mesg_showed_times = 0
        time.sleep(0.5)

        # Get shell size
        self.clear()
        print(CommandLineInterface.strWomanSword)
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines
        time.sleep(0.5)

        # Clean user actions
        self.readUserAction();

    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        elif keyboard.kbhit():
            return keyboard.getch()

    def doAction(self, action: bytes, player: PlayerCharacter):
        if not self.last_frame:
            return
        elif action == ('w' or 'W'):
            player.move_north(self.last_frame.area)
        elif action == ('a' or 'A'):
            player.move_west(self.last_frame.area)
        elif action == ('s' or 'S'):
            player.move_south(self.last_frame.area)
        elif action == ('d' or 'D'):
            player.move_east(self.last_frame.area)
        elif action == (' '):
            player.active_action_menu(self.last_frame.area)
        elif action and ord(action) == 27:
            player.active_pause_menu()

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

        # Call super method without return to avoid premature game exit
        super().manage_exceptions(ex)

        # If KeyboardInterrupt do not exit the game
        if isinstance(ex, KeyboardInterrupt):
            return False

        # Show exception info
        else:
            msg = "An error ocurrer during the game\n"
            msg += str(format_exc()) + "\n"
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
        """ This is the main method to rende all player related frames (status, equipment and quests) """
        pj_str = str()
        if frame.player:
            pj = frame.player
            # Name and position
            pj_str += style.CBOLD + ("\n[> %s (%s) <]") % (pj.name, pj.get_level()) + style.CEND
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
            pj_str += style.CGREEN + "\n Strength:" + str(pj.get_strength())
            pj_str += style.CBLUE2 + "\n Speed:" + str(round(pj.get_speed(),2)) + style.CEND
            # Player equipment
            pj_str += self.__player_equipment_str(pj)
            # Quests
            if pj.quests:
                pj_str += "\n" + style.CBOLD + "[> Quest <]" + style.CEND
                for q in pj.quests:
                    if not q.objective.done:
                        pj_str += "\n " + q.name 
                        pj_str += " "
                        pj_str += q.description
        return pj_str

    def __player_equipment_str(self, pj: PlayerCharacter):
        """ This method renders player equipment frame as a string """
        # Player equipment
        pj_str = "\n" + style.CBOLD + "[> Equipment <]\n" + style.CEND
        # Prepare each part text
        strHead = " Head(" + str(pj.items[BodyParts.head] or '-') + ") "
        strShoulder = " Shoulders(" + str(pj.items[BodyParts.shoulder] or '') + ") "
        strChest = " Chest(" + str(pj.items[BodyParts.chest] or '-') + ") "
        strBack = " Back(" + str(pj.items[BodyParts.back] or '-') + ") "
        strArms = " Arms(" + str(pj.items[BodyParts.arms] or '-') + ") "
        strHands = " Hands(" + str(pj.items[BodyParts.hands] or '-') + ") "
        strCore = " Core(" + str(pj.items[BodyParts.core] or '-') + ") "
        strLegs = " Legs(" + str(pj.items[BodyParts.legs] or '-') + ") "
        strFeets = " Feets(" + str(pj.items[BodyParts.feets] or '-') + ") "
        strEmpty = " "
        # Calculate the properly position for each part at the left side
        max_space = max(len(strHead), len(strChest), len(strArms), len(strCore), len(strFeets))
        strHead = " " * (max_space - len(strHead)) + strHead
        strChest = " " * (max_space - len(strChest)) + strChest
        strCore = " " * (max_space - len(strCore)) + strCore
        strArms = " " * (max_space - len (strArms)) + strArms
        strEmpty = " " * (max_space)
        strFeets = " " * (max_space - len(strFeets)) + strFeets
        # Compose body model with equipment
        pj_str += "\n"+style.CITALIC+strHead +style.CEND+style.CVIOLET+"    O    "+style.CEND+strShoulder
        pj_str += "\n"+style.CITALIC+strChest+style.CEND+style.CVIOLET+"  ó(w)ò  "+style.CEND+strBack
        pj_str += "\n"+style.CITALIC+strArms +style.CEND+style.CVIOLET+"_/ | | \_"+style.CEND+strHands
        pj_str += "\n"+style.CITALIC+strCore +style.CEND+style.CVIOLET+"  .|_|.  "+style.CEND
        pj_str += "\n"+style.CITALIC+strEmpty+style.CEND+style.CVIOLET+"   v v   "+style.CEND+strLegs
        pj_str += "\n"+style.CITALIC+strFeets+style.CEND+style.CVIOLET+"  _l l_  "+style.CEND+"\n"
        return pj_str

    def __area_str(self, frame: Frame):
        """ This method renders the room (area) frame """
        frame_str = str()
        if frame.area:
            # Print area type
            frame_str += style.CBOLD + "[> Area: " + area_types.NAMES[frame.area.type] + " <]" + style.CEND
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
        """ This method renders actions menu (pause menu, interactions with environment and NPCs) """
        frame_str = str()
        if frame.menu:
            frame_str +=  "\n" + style.CBOLD + "[> " + frame.menu.title + " <]" + style.CEND
            if frame.menu.options:
                frame_str += "\n"
                for option in frame.menu.options:
                    frame_str += style.CBOLD + style.CGREEN+" %s." % (frame.menu.options.index(option)) + style.CEND 
                    frame_str += style.CITALIC + "%s" % (option) + style.CEND
            frame_str += "\n" + frame.menu.query + style.CEND

        return frame_str

    def __message_str(self, frame: Frame):
        frame_str = str()

        # Get all active messages
        msgs = frame.get_msg()
        # If any
        if len(msgs) > 0:
            # Show prompt
            frame_str += "\n" + style.CBOLD + "[> Log <]" + style.CEND

            # Add messages
            for msg in msgs:
                frame_str += "\n" + style.CGREEN + " - " + style.CEND
                frame_str += style.CITALIC + msg

        return frame_str + style.CEND
