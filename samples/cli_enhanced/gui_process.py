import multiprocessing
from multiprocessing.queues import Queue
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.frame import Frame

from samples.cli_enhanced.area_box import AreaBox
from samples.cli_enhanced.command_line_box import CommandLineBox
from samples.cli_enhanced.menu_box import MenuBox
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.stats_box import PjStatsBox


class gui_process(multiprocessing.Process):


    def __init__(self, height, width):
        super().__init__()

        # Assign console sizes
        self.height = height
        self.width = width
        self.scale_width = 7
        self.scale_height = 3

        # Calculate frame sizes for each part
        self.area_container = AreaBox(self.width, 2*self.height/3, self.scale_width, self.scale_height)
        self.status_container = PjStatsBox(self.width, self.height/4)
        self.menu_container = MenuBox(self.width, self.height/8)
        self.isStarted = False

        self.frame_queue: Queue[Frame] = multiprocessing.Queue()
        self.frame = None

    def update_frame(self, frame: Frame):
        self.frame_queue.put(frame)

    def start(self):
        self.isStarted = True
        super().start()

    def stop(self):
        self.isStarted = False

    def run(self):
        while(self.isStarted):
            self.frame = self.frame_queue.get()
            if self.frame is not None:
                # Compose entire screen output (str)
                str_gui=''

                # Get stats
                str_gui += self.status_container.render(self.frame.player, self.frame.get_msg())

                # Get Area
                str_gui += self.area_container.render(self.frame)
                  
                # Get Menu
                str_gui += self.menu_container.render(self.frame.menu)
    
                remain_size = int(self.height - str_gui.count("\n")-2)
                #Print and reset cursor to console top-left
                cursor_top = ""#'\033[0;0H'
                print(cursor_top + str_gui+("\n"*remain_size) + self.debug(self.frame.player), end="\r")

    def debug(self, pj: PlayerCharacter):
        str_dbg = style.CITALIC + style.CYELLOW
        str_dbg += "Q full " + str(self.frame_queue.full()) + " size " + str(self.frame_queue.qsize())
        if pj: 
            str_dbg += " pos "+ str(pj.position) 
            if (pj.is_moving):
                str_dbg += " d %.3f" % (pj.last_distance) 
                str_dbg += " t %.3f" % (pj.delta_time) 
                str_dbg += " s %.3f" % (pj.last_distance / pj.delta_time if pj.last_distance and pj.delta_time else 0) 
        return str_dbg + style.CEND


