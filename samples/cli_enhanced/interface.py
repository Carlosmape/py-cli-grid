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
        sleep(1)
        CommandLineInterface.loaded = True
        sleep(1)
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
            
    def render(self, frame:Frame):
        self.gui_thread.update_frame(frame)

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

        # If KeyboardInterrupt do not exit the game
        if isinstance(ex, KeyboardInterrupt):
            return False

        # Show exception info
        else: 
            # Call super method without return to avoid premature game exit
            super().manage_exceptions(ex)

            msg = "An error ocurrer during the game\n"
            msg += str(format_exc()) + "\n"
            msg += "Aborting the game execution"
            input(msg)
            return True

    def end(self):
        self.gui_thread.terminate()
