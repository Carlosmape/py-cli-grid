from engine.characters.AnimalCharacter import AnimalCharacter
from engine.characters.Base import DIRECTION_EAST, DIRECTIONS, Character
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts
from engine.items.Item import Item
from engine.items.impassables.ImpassableItem import ImpassableItem
from engine.items.interactives.CollectibleItem import CollectibleItem, DecorationItem
from engine.items.interactives.Door import Door
from engine.items.interactives.Potion import Potion
from engine.items.interactives.WearableItem import FeetsWearable, HandsWearable, WearableItem
from engine.items.interactives.containeritem import container_item
from samples.cli_enhanced.render.animal_render import animal_render
from samples.cli_enhanced.render.decoration_render import decoration_render
from samples.cli_enhanced.render.door_render import door_render
from samples.cli_enhanced.render.equipment_render import equipment_render
from samples.cli_enhanced.render.generic_render import generic_render
from samples.cli_enhanced.render.potion_render import potion_render
from .pj_render import character_render
from .env_render import env_render
from .wall_render import wall_render
from .container_render import container_render
from .tittle_render import tittle_render
from .colors import style

class render_engine():
    
    background_col = style.CBEIGEBG2
    grass_col = style.CBEIGE
    wall_col = style.CBLACK

    _instance = None

    def __init__(self, ground):
        self._initialized = True
        self._object_models = {}
        self._reder_pj = character_render(render_engine.background_col, style.CBLACK)
        self._tittle_render = tittle_render(render_engine.background_col, style.CBLACK)
        self._ground_variety = ground
        self._ground_render = []
        for i in range(self._ground_variety+1):
            self._ground_render.append(env_render(render_engine.background_col, render_engine.grass_col))
            
    def render_tittle(self, loaded:bool):
        return self._tittle_render.render(loaded)
    
    def render_ground(self,ground):
        return self._ground_render[ground].render()

    def render_item(self, item:Item):
        if type(item) not in self._object_models:
            if isinstance(item, ImpassableItem):
                self._object_models[type(item)] = wall_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, Door):
                self._object_models[type(item)] = door_render(style.CYELLOWBG, render_engine.wall_col)
            elif isinstance(item, container_item):
                self._object_models[type(item)] = container_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, DecorationItem):
                self._object_models[type(item)] = decoration_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, Potion):
                self._object_models[type(item)] = potion_render(render_engine.background_col, render_engine.wall_col, item)
            elif isinstance(item, WearableItem):
                self._object_models[type(item)] = equipment_render(render_engine.background_col, render_engine.wall_col, item)
            else:
                self._object_models[type(item)] = generic_render(render_engine.background_col, style.CBLACK)
        return self._object_models[type(item)].render()
    
    def render_character(self, pj: Character):
        if isinstance(pj, NoPlayerCharacter):
            if pj not in self._object_models:
                self._object_models[pj] = character_render(render_engine.background_col, style.CBLACK)

            weapon = pj.items[BodyParts.hands]!=HandsWearable.Staff() if pj.items[BodyParts.hands] else None
            self._object_models[pj].update_equipment(pj.items[BodyParts.chest],pj.items[BodyParts.legs],weapon)
            self._object_models[pj].update_state(pj.last_direction == DIRECTIONS[DIRECTION_EAST], pj.is_moving, pj.is_attacking, pj.is_dead)

        elif isinstance(pj, AnimalCharacter):
            if pj not in self._object_models:
                self._object_models[pj] = animal_render(render_engine.background_col, style.CBLACK)

            self._object_models[pj].update_state(pj.last_direction == DIRECTIONS[DIRECTION_EAST], pj.is_moving, pj.is_attacking, pj.is_dead)

        return self._object_models[pj].render()

    def render_player(self, pj: PlayerCharacter):
        weapon = pj.items[BodyParts.hands]!=HandsWearable.Staff() if pj.items[BodyParts.hands] else None
        self._reder_pj.update_equipment(pj.items[BodyParts.chest],pj.items[BodyParts.legs], weapon)
        self._reder_pj.update_state(pj.last_direction == DIRECTIONS[DIRECTION_EAST], pj.is_moving, pj.is_attacking, pj.is_dead)
        return self._reder_pj.render()
        

