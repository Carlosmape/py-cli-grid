from multiprocessing.context import Process
from engine.frame import Frame
from samples.cli_enhanced.gui.base_game_process import base_game_process
from samples.cli_enhanced.gui.gui_process import gui_process
from samples.cli_enhanced.gui.sound_process import sound_process


class game_process(base_game_process):
    def __init__(self, height, width):
        super().__init__("GameProcess")
        self.gui_process = gui_process(height, width)
        self.sound_process = sound_process()

    def run_specific(self, frame: Frame):
        #sp = []
        #sp.append(Process(target=self.gui_process.render, args=[frame, self.frame_queue.qsize()], daemon=True))
        #sp.append(Process(target=self.sound_process.render, args=[frame], daemon=True))
        #for p in sp:
        #    p.start()
        #for p in sp:
        #    p.join()
        self.gui_process.render(frame, self.frame_queue.qsize())
        self.sound_process.render(frame)
