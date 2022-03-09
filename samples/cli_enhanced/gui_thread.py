from threading import Lock, Thread
from engine.frame import Frame

from samples.cli_enhanced.area_box import AreaBox
from samples.cli_enhanced.command_line_box import CommandLineBox
from samples.cli_enhanced.menu_box import MenuBox
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.stats_box import PjStatsBox


class gui_thread(Thread):
    def __init__(self, height, width):
        super().__init__()

        # Assign console sizes
        self.height = height
        self.width = width
        self.scale_width = 7
        self.scale_height = 3

        # Calculate frame sizes for each part
        self.area_container = AreaBox(self.width, self.height/2, self.scale_width, self.scale_height)
        self.status_container = PjStatsBox(self.width, self.height/6)
        self.menu_container = MenuBox(self.width, self.height/6)
        self.log_container = CommandLineBox(self.width, self.height/6)
        self.frame = None
        self.frame_lock = Lock()
        self.isStarted = False

    def update_frame(self, frame: Frame):
        #if self.frame_lock.acquire():
        self.frame = frame
        #    self.frame_lock.release()

    def start(self):
        self.isStarted = True
        super().start()

    def stop(self):
        self.isStarted = False

    def run(self):
        print("Thread starts...")
        while(self.isStarted):
            if self.frame is not None:
                # Compose entire screen output (str)
                str_gui=''
    
                # Get Area
                str_gui += self.area_container.render(self.frame)
    
                # Get messages
                #TODO: extract this in renfer_engine
                if self.frame:
                    composed_stats = self.frame.get_msg()
                    frame_str = style.CBOLD + "Log:" + style.CEND +"\n"
                    for msg in composed_stats[0:int(self.log_container.height-1)]:
                        frame_str += style.CGREEN + " - " + style.CEND
                        frame_str += style.CITALIC + msg + "\n"
                    str_gui += self.log_container.render(frame_str)
    
                # Get stats
                str_gui += self.status_container.render(self.frame.player)
    
                # Get Menu
                str_gui += self.menu_container.render(self.frame.menu)
    
                remain_size = int(self.height - str_gui.count("\n")-1)
                print(str_gui+"\n"*remain_size, end='\r')
        print(".. Thread terminates")
