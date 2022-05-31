from engine.frame import Frame
from .sounds.char_sounds import char_sounds
from .sounds.env_sounds import env_sounds

class sound_process():
    def __init__(self) -> None:
        super().__init__()

        # Game
        # Environment:
        self.env_sounds = env_sounds()
        # Player actions:
        self.char_sounds = char_sounds()

    def render(self, frame: Frame): 
        if frame.area:
            self.env_sounds.update(frame.area)
        if frame.player:
            self.char_sounds.update(frame.player)

