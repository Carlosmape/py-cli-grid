from random import randint
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts
from .game_sound import game_sound



class char_sounds:
    PATH_CHAR = "../assets/sounds/char/"
    PATH_FIGHT = PATH_CHAR + "fight/"

    def __init__(self) -> None:
        self.walk = [
            game_sound(char_sounds.PATH_CHAR + "walk.mp3"),
            game_sound(char_sounds.PATH_CHAR + "walk_alt.mp3"),
        ]
        self.breath = [
            game_sound(char_sounds.PATH_CHAR + "breath_slow.wav"),
        ]
        self.punch_hit = [
            game_sound(char_sounds.PATH_FIGHT + "punch_air.mp3", False),
            game_sound(char_sounds.PATH_FIGHT + "punch_air_alt.mp3", False),
        ]
        self.sword_hit = [
            game_sound(char_sounds.PATH_FIGHT + "sword_impact.mp3", False),
            game_sound(char_sounds.PATH_FIGHT + "sword_armor_impact.wav", False),
        ]

    def update(self, pj: PlayerCharacter):
        # Walking
        if pj.is_moving:
            self.walk[pj.last_direction % len(self.walk)].play()
        else:
            for s in self.walk:
                s.stop()
        # Hitting
        if pj.is_attacking:
            if not pj.items[BodyParts.hands]:
                n = randint(0, len(self.punch_hit) - 1)
                self.punch_hit[n].play()
            else:
                n = randint(0, len(self.sword_hit) - 1)
                self.sword_hit[n].play() 
        # Low-health
        if pj.stats().health() <= pj.stats().max_health()/4:
            self.breath[0].play()
        else:
            self.breath[0].stop()

