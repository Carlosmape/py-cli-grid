from random import randint
from engine.characters.Base import Character
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.Actions import Action
from engine.defines.defines import BodyParts
from engine.items.Item import Item
from engine.items.impassables.ImpassableItem import ImpassableItem
from engine.items.interactives.CollectibleItem import CollectibleItem
from engine.menu import Menu
from .pj_render import character_render
from .env_render import env_render
from .wall_render import wall_render
from .item_render import item_render
from .colors import style

class render_engine():

    def __init__(self, ground):
        self._initialized = True
        self._rendered_objects = {}
        self._reder_pj = character_render()
        self._ground_variety = ground
        self._ground_render = []
        for i in range(0,self._ground_variety+1):
            self._ground_render.append(env_render())
            
    
    def render_ground(self,ground):
        return self._ground_render[ground].render()

    def render_item(self, item:Item):
        if type(item) not in self._rendered_objects:
            if isinstance(item, ImpassableItem):
                self._rendered_objects[type(item)] = wall_render()
            else:
                self._rendered_objects[type(item)] = item_render()
        return self._rendered_objects[type(item)].render()
    
    def render_character(self, pj: NoPlayerCharacter):
        if pj not in self._rendered_objects:
            self._rendered_objects[pj] = character_render()

        self._rendered_objects[pj].update_state(True, pj.is_moving, False)
        return self._rendered_objects[pj].render()

    def render_player(self, pj: PlayerCharacter):
        self._reder_pj.update_equipment(pj.items[BodyParts.chest],pj.items[BodyParts.legs],pj.items[BodyParts.hands])
        self._reder_pj.update_state(True, pj.is_moving, False)
        return self._reder_pj.render()
        
    def render_menu(self, menu: Menu):
        composed_menu = []

        str_opt=''
        if menu.options:
            i = 0
            for opt in menu.options:
                str_opt += style.CGREEN + str(i)+ "." + style.CEND + str(opt) +" "
                i += 1        

        # Calculate elements size to center the menu
        size_menu = len(menu.title)
        size_query = len(menu.query)
        size_options = len(str_opt)
        max_size_part = max(size_menu, size_options, size_query)

        composed_menu.append(" "*int((max_size_part-size_menu)/2)+style.CBOLD+style.CITALIC+menu.title+style.CEND)
        composed_menu.append(" "*int((max_size_part-size_options)/2)+str_opt)
        composed_menu.append(" "*int((max_size_part-size_query)/2)+menu.query)
        return composed_menu


