from datetime import datetime
import lzma
import os
import pickle
import sys
from time import sleep
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.Cofiguration import Config
from engine.frame import Frame
from engine.interface import GUI
from engine.lore.GameGuide import GameGuide
from engine.menu import Menu, MenuLoadGame, MenuNewCharacter, MenuPause
from engine.repositories.GameRepository import GameRepository
from engine.world.AreaTypes import AreaTypes
from engine.world.world import World
from samples.cli_enhanced.GameFrame import GameFrame
from samples.cli_enhanced.ui.game_process import game_process
from samples.cli_enhanced.ui.input.KBHit import KBHit
from samples.cli_enhanced.ui.loading_process import loading_process


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
            Config.GameGuide.enabled = False
            Config.Stats.movement_speed = 3
            Config.Area.default_initial = AreaTypes.CITY
            Config.WorldTime.time_speed *= 10
            Config.WorldTime.initial_hour = 10


        # Initialize keyboard
        self.keyboard = KBHit()
        # Engine specific configurations
        Config.Position.tolerance = 0

        # Create Game subprocess
        # Game's settings must be beforpe start subprocess
        # Loading subprocess
        self.loading_process = loading_process(self.width, self.height)
        self.loading_process.start()
        # Main subprocess
        self.game_process = game_process(self.height, self.width)
        self.showmap = False

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

        self.game_process.start()

    def toggle_map(self):
        self.showmap = not self.showmap

    def initialize(self) -> World:
        return self.loadGame()

    def render(self, frame: Frame):
        self.game_process.update(GameFrame(frame, self.showmap))

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
            player.attack(player.nearby_npcs)
        elif action == ('m' or 'M'):
            self.toggle_map()
        elif action and ord(action) == 27:
            player.active_pause_menu()
        elif action is None:
            player.DoNothing()

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
        self.game_process.terminate()

    def selectSavedGame(self):
        """This method shows a menu to select an stored games
        and returns the save data to be loaded or 0 to begin
        a new one"""

        if os.path.isdir(Config.save_path) and os.listdir(Config.save_path) != []:
            # Compose the menu
            lOptions = ["New game"]
            lOptions += os.listdir(Config.save_path)
            iSelectedGame = int(
                self.displayMenu(MenuLoadGame(lOptions)))
            if iSelectedGame != 0:
                return lOptions[iSelectedGame]
        return 0

    def initializeNewGame(self):
        """Initializes a empty world with a new Lore and more"""
        # Ask user to insert player name
        pj_name = self.displayMenu(MenuNewCharacter())
        if not pj_name:
            pj_name = "Unnamed"
        # All ready lets feedback to the player
        menu = Menu("Somewhere, sometime, someone ...",
                    pj_name + ": Oh... What a headache... " +
                    "Shit! I dont't remember anything...\n" +
                    "Maybe someone could help me.\n" +
                    "I am completely nude in an unknown area...\n" +
                    "I should find some clothes to wear... ")
        self.displayMenu(menu)
        return World(pj_name)

    def initializeSavedGame(self, savedGame):
        """Loads a world from saved game (areas, Lore and more)"""
        with lzma.open(Config.save_path + savedGame, 'rb') as f:
            wrld = pickle.load(f)
            # Restore static values
            GameRepository.worldtime = wrld.worldtime
            GameGuide._step = wrld.game_guide_step
            return wrld

    def saveGame(self, wrld: World):
        """ Saves a binary file with current world status """
        if not os.path.exists(Config.save_path):
            os.mkdir(Config.save_path)
        
        # Retrieve static class members to allow save them values
        wrld.game_guide_step = GameGuide._step
        wrld.worldtime = GameRepository.worldtime

        filename = Config.save_path + wrld.pj.name + \
            datetime.now().strftime('_%d%m%y_%H%M%S') + ".xz"

        with lzma.open(filename, 'wb') as f:
            pickle.dump(wrld, f)
        return filename

    def loadGame(self) -> World:
        """This method checks if a saved game exists and shows
        a menu to allow user to select one (or begin a new one)"""

        iSelectedGame = self.selectSavedGame()
        if iSelectedGame == 0:
            return self.initializeNewGame()
        else:
            return self.initializeSavedGame(iSelectedGame)


