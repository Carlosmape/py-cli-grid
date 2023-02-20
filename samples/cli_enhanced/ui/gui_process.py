import threading
from time import time
import sys
from engine.defines.Actions import Walk
from engine.defines.CharacterActions import AttackCharacter
from engine.defines.ItemActions import AttackItem
from engine.defines.Translator import Translator
from engine.frame import Frame
from engine.world.AreaTypes import AreaTypes
from samples.cli_enhanced.InteractionKeys import ACTION_MENU, ATTACK, DISPLAY_MODE, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, SHOW_HELP, SHOW_MAP
from samples.cli_enhanced.ui.graphics.cli_grid.equipment_box import EquipmentBox
from .graphics.colors import style
from .graphics.cli_grid.command_line_box import CommandLineBox
from .graphics.cli_grid.area_box import AreaBox
from .graphics.cli_grid.map_box import MapBox
from .graphics.cli_grid.menu_box import MenuBox
from .graphics.cli_grid.stats_box import PjStatsBox

class ReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: str = ''

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


class gui_process():
    
    EXPANDED_HELP = style.CITALIC + f"({SHOW_HELP}) HELP: ({ACTION_MENU}) = Action Menu | () Pause Menu | ({MOVE_LEFT},{MOVE_DOWN},{MOVE_UP},{MOVE_RIGHT}) Move | ({ATTACK}) Attack | ({SHOW_MAP}) Toggle Map | ({DISPLAY_MODE}) Change status bar mode"
    COLLAPSED_HELP = style.CITALIC + f"({SHOW_HELP}) HELP toggle"

    def __init__(self, height, width, translator: Translator):
        super().__init__()
        # Translator
        self.translator = translator

        # Assign console sizes
        self.height = height
        self.width = width
        self.scale_width = 7
        self.scale_height = 3

        # Need to print rendered parts in whole screen
        self.screen = CommandLineBox(self.width, self.scale_height)

        # Calculate frame sizes for each part
        self.area_container = AreaBox(
            self.width, 2*self.height/3, self.scale_width, self.scale_height)
        self.map_container = MapBox(self.width, 2*self.height/3)
        self.equipment_container = EquipmentBox(self.width, 2*self.height/3, translator)

        self.status_container = PjStatsBox(self.width, self.height/6)
        self.menu_container = MenuBox(self.width, self.height/6, translator)
        self.last_frame = time()
        self.max_frame_delay = 0

    def render(self, show_map:bool, show_help:bool, stats_mode: int, f: Frame, q_size, fps):
        # Compose entire screen output (str)

        dbg_th = ReturnValueThread(target=self.debug, args=(f, q_size, fps))
        dbg_th.start()

        # if f.menu and isinstance(f.menu, EquipmentMenu):
        #     area_th = ReturnValueThread(target=self.equipment_container.render, args=(f,))
        if show_map:
            area_th = ReturnValueThread(target=self.map_container.render, args=(f,))
        else:
            area_th = ReturnValueThread(target=self.area_container.render, args=(f,))
        area_th.start()

        menu_th = ReturnValueThread(target=self.menu_container.render, args=(f, dbg_th.join()))
        menu_th.start()

        stats_th = ReturnValueThread(target=self.status_container.render, args=(f.player, f.public_msg + f.client_msg, stats_mode))
        stats_th.start()


        stats = stats_th.join()
        menu = menu_th.join()
        area = area_th.join()
        
        print(self.screen.render("%s%s%s%s" % (stats, area, menu, self.help(show_help) if f.area else str())))

    def help(self, show_help):
        if show_help:
            return gui_process.EXPANDED_HELP
        else:
            return gui_process.COLLAPSED_HELP

    def debug(self, frame: Frame, q_size, fps):
        str_dbg = str()
        if frame:
            str_dbg = style.CITALIC + style.CYELLOW
            str_dbg += f"Queue:%2d FPS:%2.2f Delay:%.2f Max:%.2f" % (q_size, fps, frame.created_time - self.last_frame, self.max_frame_delay)
            if frame.area and frame.created_time - self.last_frame > self.max_frame_delay:
                self.max_frame_delay = frame.created_time - self.last_frame
            self.last_frame = frame.created_time

            if frame.area:
                a = frame.area
                str_dbg += " | Area:" + \
                    AreaTypes.NAMES[a.type] + " " + \
                    str(a.width) + "x" + str(a.height) + " " + \
                    "%2.2fºC" % frame.area.weather.temperature

            if frame.player:
                pj = frame.player
                str_dbg += "\nPJ:" + str(pj.position)
                # str_dbg += " act:" + str(pj.last_action[0]) + "res:" + str(pj.last_action[1].done) + " " +pj.last_action[1].message
                str_dbg += " act:" + self.translator.get().traduce(pj.last_action[0], pj.last_action[1].done)
                if isinstance(pj.last_action[0], Walk) and pj.last_action[1].done:
                    str_dbg += " d:%.1f" % (pj.last_distance)
                    str_dbg += " t:%.1f" % (pj.delta_time)
                    str_dbg += " s:%.1f" % (pj.last_distance /
                                        pj.delta_time if pj.last_distance and pj.delta_time else 0)
                elif isinstance(pj.last_action[0], AttackCharacter) and pj.last_action[1].done:
                    str_dbg += " to " + pj.last_action[0].target.name + (" %.2f" % pj.last_action[0].target.stats().health())
                elif isinstance(pj.last_action[0], AttackItem) and pj.last_action[1].done:
                    str_dbg += " to " + self.translator.get().traduce_item_name(pj.last_action[0].item)

            str_dbg += "\nWorldTime:%d/%d %2d:%2d:%2d" % (frame.worldtime.day, frame.worldtime.year, frame.worldtime.hour, frame.worldtime.minute, frame.worldtime.second)
            str_dbg += " Night" if frame.worldtime.is_night() else " Day"
            str_dbg += f" NightStarts:{frame.worldtime.night_starts}"
            str_dbg += f" NightEnds:{frame.worldtime.night_ends}"

        return str_dbg + style.CEND + "\n"
