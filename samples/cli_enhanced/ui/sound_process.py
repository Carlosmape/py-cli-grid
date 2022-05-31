from engine.frame import Frame
from .sounds.game_sounds import game_sounds
from .sounds.char_sounds import char_sounds
from .sounds.env_sounds import env_sounds

class sound_process():
    def __init__(self) -> None:
        super().__init__()

        # Game
        self.game_sounds = game_sounds()
        # Environment:
        self.env_sounds = env_sounds()
        # Player actions:
        self.char_sounds = char_sounds()

    def render(self, frame: Frame): 
        self.game_sounds.update(frame)
        if frame.area:
            self.env_sounds.update(frame.area, frame.worldtime)
        if frame.player:
            self.char_sounds.update(frame.player)

