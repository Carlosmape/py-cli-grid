from engine.frame import Frame
from engine.world.area_types import area_types
from samples.cli_enhanced.gui.base_game_process import base_game_process

from samples.cli_enhanced.gui.graphics.render.colors import style
from samples.cli_enhanced.gui.graphics.cli_grid.area_box import AreaBox
from samples.cli_enhanced.gui.graphics.cli_grid.menu_box import MenuBox
from samples.cli_enhanced.gui.graphics.cli_grid.stats_box import PjStatsBox

class gui_process(base_game_process):

    def __init__(self, height, width):
        super().__init__()

        # Assign console sizes
        self.height = height
        self.width = width
        self.scale_width = 7
        self.scale_height = 3

        # Calculate frame sizes for each part
        self.area_container = AreaBox(
            self.width, 2*self.height/3, self.scale_width, self.scale_height)
        self.status_container = PjStatsBox(self.width, self.height/4)
        self.menu_container = MenuBox(self.width, self.height/12)

    def run_specific(self, frame: Frame):
        # Compose entire screen output (str)
        str_gui = ''

        # Player stats, journal and log
        str_gui += self.status_container.render(
            frame.player, frame.get_msg())

        # Area
        str_gui += self.area_container.render(frame)

        # Menu
        str_gui += self.menu_container.render(frame.menu)

        # Debugging info
        str_gui += self.debug(frame)

        remain_size = int(self.height - str_gui.count("\n")-1)
        # Print and reset cursor to console top-left
        cursor_top = ""  # '\033[0;0H'
        print(cursor_top + str_gui+("\n"*remain_size), end="\r")

    def debug(self, frame: Frame):
        str_dbg = str()
        if frame:
            str_dbg = style.CITALIC + style.CYELLOW
            str_dbg += "FrameQueue: " + str(self.frame_queue.qsize()) + " "
            if frame.player:
                pj = frame.player
                str_dbg += "PJ: " + str(pj.position)
                if (pj.is_moving):
                    str_dbg += " d %.3f" % (pj.last_distance)
                    str_dbg += " t %.3f" % (pj.delta_time)
                    str_dbg += " s %.3f" % (pj.last_distance /
                                            pj.delta_time if pj.last_distance and pj.delta_time else 0)
            if frame.area:
                a = frame.area
                str_dbg += " Area: " + \
                    area_types.NAMES[a.type] + " " + \
                    str(a.width) + "x" + str(a.height)
        return str_dbg + style.CEND + "\n"
