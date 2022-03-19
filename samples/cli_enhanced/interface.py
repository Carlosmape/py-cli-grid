import os
import threading
from time import sleep
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import Position, Position_types
from engine.frame import Frame
from engine.interface import GUI
from KBHit import KBHit
from engine.menu import Menu
from samples.cli_enhanced.area_box import AreaBox
from samples.cli_enhanced.command_line_box import CommandLineBox
from samples.cli_enhanced.loading_box import LoadingBox
from samples.cli_enhanced.menu_box import MenuBox
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.render.render_engine import render_engine
from samples.cli_enhanced.stats_box import PjStatsBox
from samples.cli_enhanced.gui_thread import gui_thread
keyboard = KBHit()
# System call
os.system("")


class CommandLineInterface(GUI):
    """Enhanced CLI interface for MotorRol"""

    loaded: bool = False

    def __init__(self):

        # Parent class initialization
        super().__init__()
        
        # Get terminal size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines

        # Create GUI thread
        self.gui_thread = gui_thread(self.height, self.width)

        # Create loading screen
        self.loading_container = LoadingBox(self.width, self.height, 7, 3)
        loading_thread = threading.Thread(target=self.render_start_screen)
        loading_thread.start()

        # Engine specific configurations
        Position.tolerance = 0
        
        
        # Change loaded flag
        sleep(1)
        CommandLineInterface.loaded = True
        sleep(1)

        # Start GUI thread
        self.gui_thread.start()

    def render_start_screen(self):
        blocked_read_input = True
        while blocked_read_input and not self.readUserAction():
            if CommandLineInterface.loaded:
                self.loading_container.complete_load()
                blocked_read_input = False
            print(self.loading_container.render())
            sleep(1/self.max_frame_rate)
            
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
