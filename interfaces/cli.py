import os
from engine.interface import Interface
from engine.frame import Frame
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines import Position
###
class keyboard():
    @staticmethod
    def read():
        if os.name in ('nt', 'dos'):
            from msvcrt import getch
            return getch()
        else:
            import sys
            from readchar import readchar
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
        strFrame = str()
        # Display PJ information
        strFrame += self.__player_str(frame)
        # Render roomw
        strFrame += self.__room_str(frame)
        # Render Menu
        strFrame += self.__menu_str(frame)
        # Render queued messages
        strFrame += self.__message_str(frame)

        return strFrame

    def __player_str(self, frame: Frame):
        strFrame = str()
        if frame.player:
            strFrame += ("%s Position(%s,%s)") % (frame.player.name, frame.player.position.posX, frame.player.position.posY)
            strFrame += ("\n\t♥: %s Agility: %s") % (frame.player.health, frame.player.agility)
        return strFrame

    def __room_str(self, frame: Frame):
        strFrame = str()
        if frame.room:
            # Its needed to draw inverted due to console works from top to down
            strFrame += "\n" + (self.strTopLimit* (3+frame.room.width)) + "\n"
            for y in range(frame.room.height, -1, -1):
                strFrame += self.strWall
                for x in range(0, frame.room.width+1, 1):
                    current_position = Position(x,y)
                    if frame.player.position == current_position:
                        strFrame += self.strPlayer
                    elif frame.get_npc(current_position):
                        strFrame += self.strNPC
                    elif current_position in frame.room.doors:
                        strFrame += self.strDoor
                    elif current_position in frame.room.items:
                        strFrame += self.strItem
                    elif current_position in frame.room.walls:
                        strFrame += self.strWall
                    else:
                        strFrame += ' '

                strFrame += self.strWall + "\n"
            strFrame += self.strBotLimit * (3+frame.room.width)
            strFrame +=  "\n Room("+str(frame.room.height) + "x" +str(frame.room.width) + ")"
            strFrame += "\n Doors: "
            for pos,door in frame.room.doors.items(): strFrame += " (%s,%s)" % (pos.posX, pos.posY)
            strFrame += "\n Items: "
            for pos,item in frame.room.items.items(): strFrame += " (%s,%s)" % (pos.posX, pos.posY)
            strFrame += "\n NPCs: "
            for pos,npc in frame.npcs: strFrame += " (%s,%s)" % (pos.posX, pos.posY)

        return strFrame

    def __menu_str(self, frame: Frame):
        strFrame = str()
        if frame.menu:
            strFrame += "-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    strFrame += "\n %s - %s" % (frame.menu.options.index(option), option)
            strFrame += "\n" + frame.menu.query

        return strFrame

    def __message_str(self, frame: Frame):
        strFrame = str()
        if frame.msgQueue:
            strFrame += "\nWORLD: " + frame.msgQueue.pop()

        return strFrame

