from random import randint
from engine.characters.Base import DIRECTION_EAST, DIRECTIONS, Character
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.Actions import Action
from engine.defines.defines import BodyParts
from engine.items.Item import Item
from engine.items.impassables.ImpassableItem import ImpassableItem
from engine.items.interactives.CollectibleItem import CollectibleItem, DecorationItem
from engine.items.interactives.Door import Door
from engine.items.interactives.WearableItem import FeetsWearable, HandsWearable
from engine.items.interactives.containeritem import container_item
from engine.menu import Menu
from samples.cli_enhanced.render.decoration_render import decoration_render
from samples.cli_enhanced.render.door_render import door_render
from .pj_render import character_render
from .env_render import env_render
from .wall_render import wall_render
from .item_render import item_render
from .container_render import container_render
from .tittle_render import tittle_render
from .colors import style

class render_engine():
    
    background_col = style.CBEIGEBG2
    grass_col = style.CBEIGE
    wall_col = style.CBLACK

    def __init__(self, ground):
        self._initialized = True
        self._rendered_objects = {}
        self._reder_pj = character_render(render_engine.background_col, style.CBLACK)
        self._tittle_render = tittle_render(render_engine.background_col, style.CBLACK)
        self._ground_variety = ground
        self._ground_render = []
        for i in range(0,self._ground_variety+1):
            self._ground_render.append(env_render(render_engine.background_col, render_engine.grass_col))
            
    def render_tittle(self, loaded:bool):
        return self._tittle_render.render(loaded)
    
    def render_ground(self,ground):
        return self._ground_render[ground].render()

    def render_item(self, item:Item):
        if type(item) not in self._rendered_objects:
            if isinstance(item, ImpassableItem):
                self._rendered_objects[type(item)] = wall_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, Door):
                self._rendered_objects[type(item)] = door_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, container_item):
                self._rendered_objects[type(item)] = container_render(render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, DecorationItem):
                self._rendered_objects[type(item)] = decoration_render(render_engine.background_col, render_engine.wall_col)
            else:
                self._rendered_objects[type(item)] = item_render(render_engine.background_col, style.CBLACK)
        return self._rendered_objects[type(item)].render()
    
    def render_character(self, pj: NoPlayerCharacter):
        if pj not in self._rendered_objects:
            self._rendered_objects[pj] = character_render(render_engine.background_col, style.CBLACK)

        self._rendered_objects[pj].update_equipment(pj.items[BodyParts.chest],pj.items[BodyParts.legs],pj.items[BodyParts.hands]==HandsWearable.Staff())
        self._rendered_objects[pj].update_state(pj.last_direction == DIRECTIONS[DIRECTION_EAST], pj.is_moving, False)
        return self._rendered_objects[pj].render()

    def render_player(self, pj: PlayerCharacter):
        self._reder_pj.update_equipment(pj.items[BodyParts.chest],pj.items[BodyParts.legs],pj.items[BodyParts.hands])
        self._reder_pj.update_state(pj.last_direction == DIRECTIONS[DIRECTION_EAST], pj.is_moving, False)
        return self._reder_pj.render()
        

