import os
import threading
from time import sleep
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import Position
from engine.frame import Frame
from engine.interface import GUI
from KBHit import KBHit
from samples.cli_enhanced.gui_process import gui_process
from samples.cli_enhanced.loading_box import LoadingBox
keyboard = KBHit()
# System call
os.system("")


class CommandLineInterface(GUI):
    """Enhanced CLI interface for MotorRol"""

    loaded: bool = False

    def __init__(self):

        # Parent class initialization
        super().__init__()
        
        self.max_frame_rate = 30
        # Get terminal size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines

        # Create loading screen
        self.loading_container = LoadingBox(self.width, self.height, 7, 3)
        loading_thread = threading.Thread(target=self.render_start_screen)
        loading_thread.start()

        # Create GUI thread
        self.gui_thread = gui_process(self.height, self.width)

        # Engine specific configurations
        Position.tolerance = 0
        
        # Change loaded flag
        CommandLineInterface.loaded = True
        loading_thread.join()

        # Start GUI thread
        self.gui_thread.start()

    def render_start_screen(self):
        user_action = None
        while True if not CommandLineInterface.loaded else user_action is None:
            print(self.loading_container.render())
            sleep(1/self.max_frame_rate)

            if CommandLineInterface.loaded:
                self.loading_container.complete_load()
                #Clear buffered user inputs
                user_action = self.readUserAction()

        #Finally clean buffered user inputs again
        self.readUserAction()
            
    def render(self, frame:Frame):
        self.gui_thread.update_frame(frame)

    def readUserAction(self, blocking: bool = False):
        try:
            if blocking:
                return input()
            elif keyboard.kbhit():
                return keyboard.getch()
        except BaseException as ex:
            self.manage_exceptions(ex)

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
        elif action == ('f' or 'F'):
            player.active_action_menu(self.last_frame.area)
        elif action and ord(action) == 27:
            player.active_pause_menu()
        elif action == None:
            player.no_move(self.last_frame.area)

    def clear(self):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')

    def manage_exceptions(self, ex: BaseException):
        msg = str(self.last_uptate) + ": "
        msg += "An error ocurrer during the game\n"
        msg += str(format_exc()) + "\n"
        msg += "Aborting the game execution"
        with open("error.log", "w") as f:
            f.write(msg)

        if isinstance(ex, KeyboardInterrupt):
            return False
        else:
            super().manage_exceptions(ex)
            return True

    def end(self):
        self.gui_thread.terminate()
