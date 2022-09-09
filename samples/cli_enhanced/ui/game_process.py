from time import time
from engine.frame import Frame
from samples.cli_enhanced.ui.base_game_process import base_game_process
from samples.cli_enhanced.ui.gui_process import gui_process
from samples.cli_enhanced.ui.sound_process import sound_process


class game_process(base_game_process):
    def __init__(self, height, width):
        super().__init__("GameProcess")
        self.gui_process = gui_process(height, width)
        self.sound_process = sound_process()

    def run(self):
        return super().run()

    def run_specific(self, frame: Frame, show_map: bool):
        self.begin_process_frame = time()
        self.gui_process.render(show_map, frame,  self.frame_queue.qsize(), 0 if self.fps_avg is 0 else 1 / self.fps_avg)
        self.sound_process.render(show_map, frame)

    def terminate(self) -> None:
        self.sound_process.stop_app()
        return super().terminate()
