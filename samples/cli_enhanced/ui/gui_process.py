from engine.frame import Frame
from engine.world.area_types import area_types

from .graphics.render.colors import style
from .graphics.cli_grid.command_line_box import CommandLineBox
from .graphics.cli_grid.area_box import AreaBox
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
        self.status_container = PjStatsBox(self.width, self.height/4)
        self.menu_container = MenuBox(self.width, self.height/12)

    def render(self, frame: Frame, q_size, fps):
        # Compose entire screen output (str)
        str_gui = ''
        str_gui += self.status_container.render(
            frame.player, frame.get_msg())
        str_gui += self.area_container.render(frame)
        str_gui += self.menu_container.render(frame.menu)
        str_gui += self.debug(frame, q_size, fps)

        print(self.screen.render(str_gui))

    def debug(self, frame: Frame, q_size, fps):
        str_dbg = str()
        if frame:
            str_dbg = style.CITALIC + style.CYELLOW
            str_dbg += f"Queue: %2d | FPS: %2.2f" % (q_size, fps)


            if frame.area:
                a = frame.area
                str_dbg += " | Area: " + \
                    area_types.NAMES[a.type] + " " + \
                    str(a.width) + "x" + str(a.height) + " " + \
                    "%2.2f ºC" % frame.area.weather.temperature


            if frame.player:
                pj = frame.player
                str_dbg += " | PJ: " + str(pj.position)
                str_dbg += " act: " + str(pj.last_action)
                if (pj.is_moving):
                    str_dbg += " d: %3.2f" % (pj.last_distance)
                    str_dbg += " t: %3.2f" % (pj.delta_time)
                    str_dbg += " s: %3.2f" % (pj.last_distance /
                                            pj.delta_time if pj.last_distance and pj.delta_time else 0)
            
            str_dbg += "\nWorldTime: %d/%d %2d:%2d:%2.2f" % (frame.worldtime.day, frame.worldtime.year, frame.worldtime.hour, frame.worldtime.minute, frame.worldtime.second)
            str_dbg += " Night" if frame.worldtime.is_night() else " Day"
            str_dbg += f" NightStarts: {frame.worldtime.night_starts}"
            str_dbg += f" NightEnds: {frame.worldtime.night_ends}"

        return str_dbg + style.CEND + "\n"
