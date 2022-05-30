import multiprocessing
from multiprocessing.queues import Queue
from typing import Type
from engine.defines.Actions import Action
from engine.frame import Frame
from samples.cli_enhanced.gui.base_game_process import base_game_process
from samples.cli_enhanced.gui.sounds.char_sounds import char_sounds
from samples.cli_enhanced.gui.sounds.env_sounds import env_sounds

class sound_process(base_game_process):
    def __init__(self) -> None:
        super().__init__()
        # Specific actions queue
        self.action_queue: Queue[Action] = multiprocessing.Queue()

        # Game
        # Environment:
        self.env_sounds = env_sounds()
        # Player actions:
        self.char_sounds = char_sounds()

    def run_specific(self, frame: Frame): 
        if frame.area:
            self.env_sounds.update(frame.area)
        if frame.player:
            self.char_sounds.update(frame.player)

