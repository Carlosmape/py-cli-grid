import threading
from engine.frame import Frame
from samples.cli_enhanced.sounds.char_sounds import char_sounds
from samples.cli_enhanced.sounds.env_sounds import env_sounds

class sound_manager():
    def __init__(self) -> None:
        # Game
        # Environment:
        self.env_sounds = env_sounds()
        # Player actions:
        self.char_sounds = char_sounds()
        self.__lock = threading.Lock()

    def update(self, frame: Frame):
        with self.__lock:
            if frame.area:
                self.env_sounds.update(frame.area)
            if frame.player:
                self.char_sounds.update(frame.player)
