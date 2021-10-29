from engine.interface import *

if os.name in ('nt', 'dos'):
    from msvcrt import getch
else:
    import getch

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
            return getch()

    def doAction(self, action, player: PlayerCharachter):
        if action == (b'w' or  b'W'):
            player.move_north()
        elif action == (b'a' or b'A'):
            player.move_west()
        elif action == (b's' or b'S'):
            player.move_south()
        elif action == (b'd' or b'D'):
            player.move_east()
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
            stringFrame += "\n"
            stringFrame += "-" * (frame.room.width + 2)
            for i in range(0, frame.room.height):
                stringFrame += "\n"+self.strVWall
                for j in range(0, frame.room.width):
                    if frame.player.position == Position(j,i):
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
