from time import time
from engine.defines.Actions import Walk
from engine.defines.CharacterActions import AttackCharacter
from engine.defines.ItemActions import AttackItem
from engine.frame import Frame
from engine.world.area_types import area_types
from .graphics.render.colors import style
from .graphics.cli_grid.command_line_box import CommandLineBox
from .graphics.cli_grid.area_box import AreaBox
from .graphics.cli_grid.map_box import MapBox
from .graphics.cli_grid.menu_box import MenuBox
from .graphics.cli_grid.stats_box import PjStatsBox

class gui_process():

    def __init__(self, height, width):
        super().__init__()

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
        self.status_container = PjStatsBox(self.width, self.height/6)
        self.menu_container = MenuBox(self.width, self.height/6)
        self.last_frame = time()
        self.max_frame_delay = 0

    def render(self, show_map:bool, f: Frame, q_size, fps):
        # Compose entire screen output (str)
        str_gui: str
        str_gui = self.status_container.render(f.player, f.get_msg())
        if show_map:
            str_gui += self.map_container.render(f)
        else:
            str_gui += self.area_container.render(f)
        str_gui += self.menu_container.render(f, self.debug(f, q_size, fps))

        print(self.screen.render(str_gui))

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
                    area_types.NAMES[a.type] + " " + \
                    str(a.width) + "x" + str(a.height) + " " + \
                    "%2.2fºC" % frame.area.weather.temperature

            if frame.player:
                pj = frame.player
                str_dbg += "\nPJ:" + str(pj.position)
                str_dbg += " act:" + str(pj.last_action)
                if pj.last_action:
                    if isinstance(pj.last_action, Walk):
                        str_dbg += " d:%.1f" % (pj.last_distance)
                        str_dbg += " t:%.1f" % (pj.delta_time)
                        str_dbg += " s:%.1f" % (pj.last_distance /
                                            pj.delta_time if pj.last_distance and pj.delta_time else 0)
                    elif isinstance(pj.last_action, AttackCharacter):
                        str_dbg += " to " + pj.last_action.target.name + (" %.2f" % pj.last_action.target.stats().health())
                    elif isinstance(pj.last_action, AttackItem):
                        str_dbg += " to " + pj.last_action.item.name

            str_dbg += "\nWorldTime:%d/%d %2d:%2d:%2d" % (frame.worldtime.day, frame.worldtime.year, frame.worldtime.hour, frame.worldtime.minute, frame.worldtime.second)
            str_dbg += " Night" if frame.worldtime.is_night() else " Day"
            str_dbg += f" NightStarts:{frame.worldtime.night_starts}"
            str_dbg += f" NightEnds:{frame.worldtime.night_ends}"

        return str_dbg + style.CEND + "\n"
