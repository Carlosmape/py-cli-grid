from engine.interface import *
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
