#!/bin/python
import sys



sys.path.append('../../')

from engine.repositories.WearableItemRepository import WearableItemRepository
from engine.repositories.CharacterRepository import CharacterRepository
from engine.repositories.CityRepository import CityRepository
from engine.repositories.FactionRepository import FactionRepository
from engine.repositories.DialogRepository import DialogElements, DialogRepository
from engine.engine import Engine
from interface import CommandLineInterface
from samples.assets.lore import characters, factions, cities, dialogs
from samples.assets.items.equipment import BACKWEARABLES, CHESTWEARABLES, FEETSWEARABLES, HANDSWEARABLES, HEADWEARABLES, LEGSWEARABLES, SHOULDERWEARABLES

if __name__ == '__main__':

    #########
    # Game specific stuff
    #########
    equipment_repo = WearableItemRepository(HEADWEARABLES, SHOULDERWEARABLES, CHESTWEARABLES, BACKWEARABLES, HANDSWEARABLES, LEGSWEARABLES, FEETSWEARABLES)

    #########
    # Run Engine
    # Interface should be changed
    #########
    interface = CommandLineInterface(equipment_repo)
    engine = Engine(
        interface,
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
        equipment_repo
    )
    engine.run()
