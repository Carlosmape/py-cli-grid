import os
import sys
import threading
from time import sleep
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import Position
from engine.frame import Frame
from engine.interface import GUI
from samples.cli_enhanced.gui.input.KBHit import KBHit
from engine.world.area import area
from samples.cli_enhanced.gui.gui_process import gui_process
from samples.cli_enhanced.gui.loading_process import loading_process
from samples.cli_enhanced.gui.sound_process import sound_process


class CommandLineInterface(GUI):
    """Enhanced CLI interface sample for MotorRol"""

    def __init__(self):
        super().__init__()

        self.max_frame_rate = 25
        # Get terminal size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines

        # Read arguments
        if "debug" in sys.argv:
            area.MIN_HEIGHT = area.MAX_HEIGHT = int(self.height/3)
            area.MIN_WIDTH = area.MAX_WIDTH = int(self.width/7)

        # Initialize keyboard
        self.keyboard = KBHit() 
        # Engine specific configurations
        Position.tolerance = 0
        

        # Create Game subprocess
        # Game's settings must be beforpe start subprocess 
        # Loading subprocess
        self.loading_process = loading_process(self.width, self.height)
        self.loading_process.start()
        # Main subprocess
        self.graphic_process = gui_process(self.height, self.width)
        self.sound_process = sound_process()

        sleep(1)
        self.loading_process.complete(None)
        sleep(1)
        # Clean user actions just before press key
        self.keyboard.getch()
        while self.loading_process.is_alive():
            self.loading_process.complete(
                self.keyboard.getch()
            )
        self.clear()

        self.sound_process.start()
        self.graphic_process.start()

    def render(self, frame: Frame):
        self.graphic_process.update(frame)
        self.sound_process.update(frame)

    def readUserAction(self, blocking: bool = False):
        try:
            if blocking:
                return input()
            elif self.keyboard.kbhit():
                return self.keyboard.getch()
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
        elif action == ('j' or 'J'):
            player.Attack(player.nearby_npcs)
        elif action and ord(action) == 27:
            player.active_pause_menu()
        elif action is None:
            player.no_move()

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
        self.loading_process.terminate()
        self.graphic_process.terminate()
        self.sound_process.terminate()
