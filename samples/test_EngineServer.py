#!/bin/python

import sys

sys.path.append('../')

from engine.EngineServer import EngineServer
from engine.Logger import Logger
from engine.defines.Cofiguration import Config
from engine.world.AreaTypes import AreaTypes
from engine.repositories.EquipmentRepository import EquipmentRepository
from engine.repositories.ItemRepository import ItemRepository
from engine.repositories.CharacterRepository import CharacterRepository
from engine.repositories.ProfessionRepository import ProfessionRepository
from engine.repositories.CityRepository import CityRepository
from engine.repositories.FactionRepository import FactionRepository
from engine.repositories.DialogRepository import DialogRepository
from engine.repositories.TerrainRepository import TerrainRepository
from engine.repositories.GameRepository import GameRepository
from engine.lore.dialogs.DialogElements import DialogElements
from samples.assets.lore import characters, factions, cities, dialogs
from samples.assets.items.equipment import LoreEquipment
from samples.assets.items.materials import LoreMaterials
from samples.assets.items.mineral import LoreMinerals
from samples.assets.items.vegetation import LoreVegetables
from samples.assets.items.wildlife import LoreWildLife
from samples.assets.items.manufactured import LoreManufactured
from samples.assets.lore.professions import MILITARIES, PRODUCERS, TRADERS, UNEMPLOYEDS


if __name__ == '__main__':

    #########
    # Game specific stuff... Repositories of all needed things in this case to render a loading screen not the engine itself
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
    GameRepository.equipment_repo = EquipmentRepository(LoreEquipment.HEADWEARABLES, LoreEquipment.SHOULDERWEARABLES, LoreEquipment.CHESTWEARABLES, LoreEquipment.BACKWEARABLES, LoreEquipment.HANDSWEARABLES, LoreEquipment.LEGSWEARABLES, LoreEquipment.FEETSWEARABLES)
    GameRepository.collectible_repo = ItemRepository(LoreVegetables.GROUNDSPAWNING + LoreMinerals.GROUNDSPAWNING + LoreWildLife.GROUNDSPAWNING,
                                                     LoreMaterials.PORTALS, LoreManufactured.DRINKABLEITEMS, LoreVegetables.EDIBLES)
    GameRepository.terrain_repo = TerrainRepository(LoreMaterials.TERRAINOBSTACLES, LoreVegetables.VEGETABLEPRODUCTORS, LoreMinerals.MINES, LoreMaterials.BUILDINGMATERIALS, LoreMaterials.DOORBUILDINGMATERIALS)

    # Setting disable decimal tolerace
    Config.Position.tolerance = 0 

    # Read arguments
    if "debug" in sys.argv:
        Config.GameGuide.enabled = False
        Config.Stats.movement_speed = 3
        Config.Area.default_initial = AreaTypes.WOOD
        Config.WorldTime.time_speed *= 10
        Config.WorldTime.initial_hour = 10
        Config.log_enabled = True
        Logger.initialize()
    # Always enable STD IO
    Config.log_to_std_io = True

    server = EngineServer()
    server.run()

