#!/bin/python
import sys

sys.path.append('../../')

from engine.repositories.EquipmentRepository import EquipmentRepository
from engine.repositories.ItemRepository import ItemRepository
from engine.repositories.CharacterRepository import CharacterRepository
from engine.repositories.ProfessionRepository import ProfessionRepository
from engine.repositories.CityRepository import CityRepository
from engine.repositories.FactionRepository import FactionRepository
from engine.repositories.DialogRepository import DialogElements, DialogRepository
from engine.repositories.TerrainRepository import TerrainRepository
from engine.repositories.GameRepository import GameRepository
from engine.engine import Engine
from interface import CommandLineInterface
from samples.assets.lore import characters, factions, cities, dialogs
from samples.assets.items.equipment import BACKWEARABLES, CHESTWEARABLES, FEETSWEARABLES, HANDSWEARABLES, HEADWEARABLES, LEGSWEARABLES, SHOULDERWEARABLES
from samples.assets.items.collectibles import ALLDECORATION, DRINKABLEITEMS, EDIBLEITEMS, PORTALS
from samples.assets.lore.professions import MILITARIES, PRODUCERS, TRADERS, UNEMPLOYEDS
from samples.assets.items.terrain import BUILDINGMATERIALS, DOORBUILDINGMATERIALS, MINERALPRODUCTORS, VEGETABLEPRODUCTORS, TERRAINOBSTACLES


if __name__ == '__main__':

    #########
    # Game specific stuff... Repositories of all needed things
    #########
    GameRepository.fact_repo = FactionRepository(factions.NAMES, factions.DESCRIPTIONS, factions.SLOGANS)
    GameRepository.city_repo = CityRepository(cities.NAMES)
    GameRepository.char_repo = CharacterRepository(characters.MALE_NAMES, characters.FEMALE_NAMES, False)
    GameRepository.prof_repo = ProfessionRepository(UNEMPLOYEDS, PRODUCERS, TRADERS, MILITARIES)
    GameRepository.dial_repo = DialogRepository(
        DialogElements(dialogs.SUSPICIOUS_GREETINGS, dialogs.NEUTRAL_GREETINGS, dialogs.FRIENDLY_GREETINGS),
        DialogElements(dialogs.SUSPICIOUS_GOODBYES, dialogs.NEUTRAL_GOODBYES, dialogs.FRIENDLY_GOODBYES),
        DialogElements(dialogs.SUSPICIOUS_TALK, dialogs.NEUTRAL_TALK, dialogs.NEUTRAL_TALK),
        dialogs.GENERIC_CONFIRMATIONS,
        dialogs.GAME_TIPS
    )
    GameRepository.equipment_repo = EquipmentRepository(HEADWEARABLES, SHOULDERWEARABLES, CHESTWEARABLES, BACKWEARABLES, HANDSWEARABLES, LEGSWEARABLES, FEETSWEARABLES)
    GameRepository.collectible_repo = ItemRepository(ALLDECORATION, PORTALS, DRINKABLEITEMS, EDIBLEITEMS)
    GameRepository.terrain_repo = TerrainRepository(TERRAINOBSTACLES, VEGETABLEPRODUCTORS, MINERALPRODUCTORS, BUILDINGMATERIALS, DOORBUILDINGMATERIALS)

    #########
    # Run Engine
    # Interface should be changed
    #########
    interface = CommandLineInterface()
    engine = Engine(interface)
    engine.run()
