from random import randint
from engine.world.area import area
from engine.world.area_types import area_types
from samples.cli_enhanced.sounds.game_sound import game_sound


class env_sounds:
    PATH_ENV = "../assets/sounds/env/"

    def __init__(self) -> None:
        self.nature = [
            game_sound(env_sounds.PATH_ENV + "nature.mp3"),
        ]
        self.people = [
            game_sound(env_sounds.PATH_ENV + "people.wav"),
            game_sound(env_sounds.PATH_ENV + "people_alt.wav"),
        ]

    def update(self, ar: area):
        if ar.type is area_types.CITY:
            n = randint(0, len(self.nature) - 1)
            self.nature[n].play()
            n = randint(0, len(self.people) - 1)
            self.people[n].play()
        else:
            n = randint(0, len(self.nature) - 1)
            self.nature[n].play()

