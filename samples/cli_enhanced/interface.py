import os
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.frame import Frame
from engine.interface import GUI
from KBHit import KBHit

keyboard = KBHit()
# System call
os.system("")

class CommandLineInterface(GUI):
    """Enhanced CLI interface for MotorRol"""

    def __init__(self):
        super().__init__()

        # Get terminal size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines - 1

        # Clear console
        self.clear() 
        # Clean user actions
        self.readUserAction();

    def render(self, frame:Frame):
        raise NotImplemented

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
