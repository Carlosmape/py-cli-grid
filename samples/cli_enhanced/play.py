#!/bin/python
import sys
sys.path.append('../../')

from engine.repositories.EquipmentRepository import EquipmentRepository
from engine.repositories.ItemRepository import ItemRepository
from engine.repositories.CharacterRepository import CharacterRepository
from engine.repositories.CityRepository import CityRepository
from engine.repositories.FactionRepository import FactionRepository
from engine.repositories.DialogRepository import DialogElements, DialogRepository
from engine.repositories.GameRepository import GameRepository
from engine.engine import Engine
from interface import CommandLineInterface
from samples.assets.lore import characters, factions, cities, dialogs
from samples.assets.items.equipment import BACKWEARABLES, CHESTWEARABLES, FEETSWEARABLES, HANDSWEARABLES, HEADWEARABLES, LEGSWEARABLES, SHOULDERWEARABLES
from samples.assets.items.collectibles import ALLDECORATION, DRINKABLEITEMS, EDIBLEITEMS
from engine.repositories.TerrainRepository import TerrainRepository
from samples.assets.items.terrain import BUILDINGMATERIALS, TERRAINOBSTACLES


if __name__ == '__main__':

    #########
    # Game specific stuff... Repositories of all needed things
    #########
    game_repo = GameRepository(
        FactionRepository(factions.NAMES, factions.DESCRIPTIONS, factions.SLOGANS),
        CityRepository(cities.NAMES),
        CharacterRepository(characters.NAMES),
        DialogRepository(
            DialogElements(dialogs.SUSPICIOUS_GREETINGS, dialogs.NEUTRAL_GREETINGS, dialogs.FRIENDLY_GREETINGS),
            DialogElements(dialogs.SUSPICIOUS_GOODBYES, dialogs.NEUTRAL_GOODBYES, dialogs.FRIENDLY_GOODBYES),
            DialogElements(dialogs.SUSPICIOUS_TALK, dialogs.NEUTRAL_TALK, dialogs.NEUTRAL_TALK),
            dialogs.GENERIC_CONFIRMATIONS,
            dialogs.GAME_TIPS
        ),
        EquipmentRepository(HEADWEARABLES, SHOULDERWEARABLES, CHESTWEARABLES, BACKWEARABLES, HANDSWEARABLES, LEGSWEARABLES, FEETSWEARABLES),
        ItemRepository(ALLDECORATION, DRINKABLEITEMS, EDIBLEITEMS),
        TerrainRepository(TERRAINOBSTACLES, BUILDINGMATERIALS)
    )

    #########
    # Run Engine
    # Interface should be changed
    #########
    interface = CommandLineInterface(game_repo)
    engine = Engine(
        interface,
        game_repo
    )
    engine.run()
