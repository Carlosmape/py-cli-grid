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
from samples.cli_enhanced.command_line_box import AreaBox, CommandLineBox, LoadingBox
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.render.render_engine import render_engine

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
        self.height = size.lines

        # Calculate scale to draw items
        self.scale_width = 7
        self.scale_height = 3

        # Calculate frame sizes for each part
        self.loading_container = LoadingBox(self.width, self.height, self.scale_width, self.scale_height)
        self.area_container = AreaBox(self.width, self.height/2, self.scale_width, self.scale_height)
        self.status_container = CommandLineBox(self.width, self.height/4)
        self.menu_container = CommandLineBox(self.width, self.height/4)

        # Items per row and col
        self.objects_per_row = int(self.width/self.scale_width)
        self.objects_per_col = int(self.height/self.scale_height)
        self.objects_in_area = self.objects_per_col*self.objects_per_row

        # Initialize Render
        self.render_engine = render_engine(self.objects_in_area)
        
        self.render_start_screen()

    def render_start_screen(self):
        while not self.readUserAction():
            print(self.loading_container.render())
            sleep(1/self.max_frame_rate)
            
    def render(self, frame:Frame):
        threading.Thread(target=self.render_thread, args=(frame,)).start()

    def render_thread(self, frame: Frame):
        str_gui=''

        # Get Area
        str_gui += self.area_container.render(frame)

        # Get stats
        #TODO: extract this in renfer_engine
        composed_stats = frame.get_msg()
        # Add messages
        frame_str = ""
        for msg in composed_stats:
            frame_str += style.CGREEN + " - " + style.CEND
            frame_str += style.CITALIC + msg + "\n"
        str_gui += self.status_container.render(frame_str)

        # Get Menu
        composed_menu = self.render_menu(frame.menu)
        if composed_menu:
            str_gui += self.menu_container.render(composed_menu[0]+"\n"+composed_menu[1]+"\n"+composed_menu[2]+"\n")

        remain_size = int(self.height - str_gui.count("\n")-1)
        print(str_gui+"\n"*remain_size, end='\r')

    
    def render_menu(self, menu:Menu):
        if not menu:
            return
        return self.render_engine.render_menu(menu)

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
