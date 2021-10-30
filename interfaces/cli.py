from engine.interface import *

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
        if action == (b'w' or  b'W'):
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
            #TODO temporary. It should raise a exit menu asking for confirmation and save game and so on
            exit() 

    def render(self, frame: Frame):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')
        print(self.convertToString(frame))

    def convertToString(self, frame: Frame):
        stringFrame = str()
        #Display PJ information
        stringFrame += self.__player_str(frame)
        # Render room
        stringFrame += self.__room_str(frame)
        # Render Menu
        stringFrame += self.__menu_str(frame)
        # Render queued messages
        stringFrame += self.__message_str(frame)

        return stringFrame

    def __player_str(self, frame: Frame):
        stringFrame = str()
        if frame.player:
            stringFrame += ("%s Position(%s,%s)") % (frame.player.name, frame.player.position.posX, frame.player.position.posY)
            stringFrame += ("\n\t♥: %s Agility: %s") % (frame.player.health, frame.player.agility)
        return stringFrame

    def __room_str(self, frame: Frame):
        stringFrame = str()
        if frame.room:
            # Its needed to draw inverted due to console works from top to down
            stringFrame += "\n" + (self.strTopLimit* (3+frame.room.width)) + "\n"
            for y in range(frame.room.height, -1, -1):
                stringFrame += self.strWall
                for x in range(0, frame.room.width+1, 1):
                    current_position = Position(x,y)
                    if frame.player.position == current_position:
                        stringFrame += self.strPlayer
                    elif frame.get_npc(current_position):
                        stringFrame += self.strNPC
                    elif current_position in frame.room.doors:
                        stringFrame += self.strDoor
                    elif current_position in frame.room.items:
                        stringFrame += self.strItem
                    elif current_position in frame.room.walls:
                        stringFrame += self.strWall
                    else:
                        stringFrame += ' '

                stringFrame += self.strWall + "\n"
            stringFrame += self.strBotLimit * (3+frame.room.width)
            stringFrame +=  "\n Room("+str(frame.room.height) + "x" +str(frame.room.width) + ")"
            stringFrame += "\n Doors: "
            for pos,door in frame.room.doors.items(): stringFrame += " (%s,%s)" % (pos.posX, pos.posY)
            stringFrame += "\n Items: "
            for pos,item in frame.room.items.items(): stringFrame += " (%s,%s)" % (pos.posX, pos.posY)
            stringFrame += "\n NPCs: "
            for pos,npc in frame.npcs: stringFrame += " (%s,%s)" % (pos.posX, pos.posY)

        return stringFrame

    def __menu_str(self, frame: Frame):
        stringFrame = str()
        if frame.menu:
            stringFrame += "-->" + frame.menu.title
            if frame.menu.options:
                for option in frame.menu.options:
                    stringFrame += "\n %s - %s" % (frame.menu.options.index(option), option)
            stringFrame += "\n" + frame.menu.query

        return stringFrame

    def __message_str(self, frame: Frame):
        stringFrame = str()
        if frame.msgQueue:
            stringFrame += "\nWORLD: " + msgQueue.pop()

        return stringFrame

