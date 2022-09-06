import multiprocessing
from time import sleep
from multiprocessing.queues import Queue

from .graphics.cli_grid.loading_box import LoadingBox
from .base_game_process import base_game_process


class loading_process(base_game_process):

    def __init__(self, width: int, height: int):
        super().__init__()

        self.flag_queue: Queue[bool] = multiprocessing.Queue()
        self.user_queue = multiprocessing.Queue()

        # Assign console sizes
        self.height = height
        self.width = width
        self.max_frame_rate = 20

        # Need to print rendered parts in whole screen
        self.screen = LoadingBox(self.width, self.height, 7, 3)

    def complete(self, user_input: str | None):
        """Completes loading screen and ps"""
        self.flag_queue.put(True)
        if user_input:
            self.user_queue.put(user_input)
        
    def run(self):
        userinput = None
        while self.is_started if not self.screen.loaded else userinput is None:
            flag = False

            try:
                flag = self.flag_queue.get_nowait()
                userinput = None
                if self.screen.loaded: 
                    userinput = self.user_queue.get_nowait()
            except:
                pass

            if flag:
                self.screen.complete_load()

            print(self.screen.render(), end="\r")
            sleep(1/self.max_frame_rate)

        self.user_queue.close()
        self.flag_queue.close()
        self.stop()
