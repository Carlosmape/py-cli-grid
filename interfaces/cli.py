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
    strVWall = '|'
    strHWall = '-'
    strPlayer = '#'
    strItem = '·'
    strNPC = 'O'
    strDoor = '*'

    # Constructor
    def __init__(self):
        print("Welcome to your CLI Adventure")
        print("Initializing interface")
        super().__init__()
        self.maxFrameRate=2
        #Get shell size
        size=os.get_terminal_size()
        self.width=size.columns
        self.height=size.lines
    
    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        else:
            return keyboard.read()

    def doAction(self, action: bytes, player: PlayerCharachter):
        if action == (b'w' or  b'W'):
            player.move_north(self.last_frame.room)
        elif action == (b'a' or b'A'):
            player.move_west(self.last_frame.room)
        elif action == (b's' or b'S'):
            player.move_south(self.last_frame.room)
        elif action == (b'd' or b'D'):
            player.move_east(self.last_frame.room)
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
        if frame.player:
            stringFrame += ("%s - Health: %s\n") % (frame.player.name, frame.player.health)
        #Render room
        if frame.room:
            stringFrame += "\n" + "-" * (frame.room.width)
            #Note: its needed to draw inversed due to 
            #console works from top to down
            print(frame.room.height, "x", frame.room.width)
            for y in range(frame.room.height, 0, -1):
                for x in range(0, frame.room.width, 1):
                    if frame.player.position == Position(x,y):
                        stringFrame += self.strPlayer
                    elif frame.room.doors.position == Position(x,y):
                        stringFrame += self.strDoor
                    elif x == 0:
                        stringFrame += "\n"+self.strVWall
                    elif x == frame.room.width-1:
                        stringFrame += self.strVWall
                    else:
                        stringFrame += ' '
            stringFrame += "\n" + "-" * (frame.room.width)
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
