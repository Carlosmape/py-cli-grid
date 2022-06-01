#!/bin/python
import sys

sys.path.append('../../')

from engine.repositories.CharacterRepository import CharacterRepository
from engine.repositories.CityRepository import CityRepository
from engine.repositories.FactionRepository import FactionRepository
from engine.engine import Engine
from interface import CommandLineInterface
from samples.assets.lore import characters, factions, cities


#########
# Run Engine
# Interface should be changed
#########
interface = CommandLineInterface()
engine = Engine(
    interface,
    FactionRepository(factions.NAMES, factions.DESCRIPTIONS, factions.SLOGANS),
    CityRepository(cities.NAMES),
    CharacterRepository(characters.NAMES)
)
engine.run()
