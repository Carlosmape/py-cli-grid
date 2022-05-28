from audioplayer import AudioPlayer
from engine.frame import Frame
from engine.world.area_types import area_types


class game_sound(AudioPlayer):
    def __init__(self, filename, loop: bool = True):
        super().__init__(filename)
        self.is_started = False
        self.is_playing = False
        self.loop = loop

    def play(self):
        if self.is_started:
            self.is_playing = True
            super().resume()
        else:
            self.is_started = self.is_playing = True
            super().play(self.loop)

    
    def stop(self):
        if self.is_playing:
            super().pause()

class sound_manager():
    def __init__(self) -> None:
        self.env_sound = game_sound("sounds/environment.mp3")
        self.walk_sound = game_sound("sounds/walk.mp3")

    def update(self, frame: Frame):
        # Environmental sound
        if frame.area:
            self.env_sound.play()
        else:
            self.env_sound.stop()

        # Character sounds
        if frame.player and \
            frame.player.is_moving:
            self.walk_sound.play()
        else:
            self.walk_sound.stop()
