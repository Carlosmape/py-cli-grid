from audioplayer import AudioPlayer

class game_sound(AudioPlayer):
    def __init__(self, filename, loop: bool = True):
        """Manages game sounds
        loop: False -> triggers the sound once"""
        super().__init__(filename)
        self.is_started = False
        self.is_playing = False
        self.loop = loop

    def play(self):
        if not self.loop:
            super().play()
        elif self.is_started:
            self.is_playing = True
            super().resume()
        else:
            self.is_started = self.is_playing = True
            super().play(self.loop)
    
    def stop(self):
        if self.loop and self.is_playing:
            super().pause()


