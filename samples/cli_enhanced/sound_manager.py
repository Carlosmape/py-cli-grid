import threading
from audioplayer import AudioPlayer
from engine.frame import Frame


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
        self.env = game_sound("sounds/environment.mp3")
        self.walk = [
            game_sound("sounds/walk.mp3"),
            game_sound("sounds/walk_alt.mp3")
        ]
        self.__lock = threading.Lock()

    def update(self, frame: Frame):
        with self.__lock:
            # Environmental sounds
            if frame.area:
                self.env.play()
            else:
                self.env.stop()
    
            # Character sounds
            if frame.player and \
                frame.player.is_moving:
                self.walk[frame.player.last_direction % len(self.walk)].play()
            else:
                for walk in self.walk:
                    walk.stop()
