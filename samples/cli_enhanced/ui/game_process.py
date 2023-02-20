from time import time
from engine.defines.Translator import Translator
from samples.cli_enhanced.GameFrame import GameFrame
from samples.cli_enhanced.ui.base_game_process import base_game_process
from samples.cli_enhanced.ui.gui_process import gui_process
from samples.cli_enhanced.ui.sound_process import sound_process


class game_process(base_game_process):
    def __init__(self, height:int , width: int, translator: Translator):
        super().__init__("GameProcess")
        self.gui_process = gui_process(height, width, translator)
        self.sound_process = sound_process()

    def run(self):
        return super().run()

    def run_specific(self, frame: GameFrame):
        self.begin_process_frame = time()
        self.gui_process.render(frame.showmap, frame.showhelp, frame.statsmode, frame.frame, self.frame_queue.qsize(), 0 if self.fps_avg is 0 else 1 / self.fps_avg)
        self.sound_process.render(frame.showmap, frame.frame)

    def terminate(self) -> None:
        self.sound_process.stop_app()
        return super().terminate()
