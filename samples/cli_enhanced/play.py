#!/bin/python
import sys

sys.path.append('../../')

from engine.lore.Repository import CharacterRepo, CityRepo, FactionRepo
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
    FactionRepo(factions.NAMES, factions.DESCRIPTIONS, factions.SLOGANS),
    CityRepo(cities.NAMES),
    CharacterRepo(characters.NAMES)
)
engine.run()
