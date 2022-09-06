from engine.characters.AnimalCharacter import AnimalCharacter
from engine.characters.Base import DIRECTION_EAST, DIRECTIONS
from engine.characters.InteractiveCharacter import InteractiveCharacter
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.Actions import AttackAny, Walk
from engine.defines.CharacterActions import BeingAttacked
from engine.defines.BodyParts import BodyParts
from engine.items.Item import Item
from engine.items.interactives.CollectibleItem import DecorationItem
from engine.items.interactives.Portal import Portal
from engine.items.interactives.EdibleItem import EdibleItem
from engine.items.interactives.DrinkableItem import DrinkableItem
from engine.items.interactives.WearableItem import WearableItem
from engine.items.interactives.ContainerItem import ContainerItem
from samples.assets.items.equipment import Staff
from samples.assets.items.terrain import Rock, RockWall, WoodWall
from samples.cli_enhanced.ui.graphics.render.rock_render import rock_render
from samples.cli_enhanced.ui.graphics.render.wood_wall_render import wood_wall_render
from .edible_render import edible_render
from .animal_render import animal_render
from .decoration_render import decoration_render
from .portal_render import portal_render
from .equipment_render import equipment_render
from .generic_render import generic_render
from .potion_render import potion_render
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
        self._reder_pj = character_render(
            render_engine.background_col, style.CBLACK)
        self._tittle_render = tittle_render(
            render_engine.background_col, style.CBLACK)
        self._ground_variety = ground
        self._ground_render = []
        for i in range(self._ground_variety + 1):
            self._ground_render.append(env_render(
                render_engine.background_col, render_engine.grass_col))

    def render_tittle(self, loaded: bool):
        return self._tittle_render.render(loaded)

    def render_ground(self, ground):
        return self._ground_render[ground].render()

    def render_item(self, item: Item):
        if type(item) not in self._object_models:
            if isinstance(item, RockWall):
                self._object_models[type(item)] = wall_render()
            elif isinstance(item, WoodWall):
                self._object_models[type(item)] = wood_wall_render()
            elif isinstance(item, Rock):
                self._object_models[type(item)] = rock_render(
                    render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, Portal):
                self._object_models[type(item)] = portal_render(
                    style.CYELLOWBG, render_engine.wall_col) 
            elif isinstance(item, DrinkableItem):
                self._object_models[type(item)] = potion_render(
                    render_engine.background_col, render_engine.wall_col, item)
            elif isinstance(item, EdibleItem):
                self._object_models[type(item)] = edible_render(
                    render_engine.background_col, render_engine.wall_col)
            elif isinstance(item, DecorationItem):
                self._object_models[type(item)] = decoration_render(
                    render_engine.background_col, render_engine.wall_col, item)
            elif isinstance(item, WearableItem):
                self._object_models[type(item)] = equipment_render(
                    render_engine.background_col, render_engine.wall_col, item)
            elif isinstance(item, ContainerItem):
                self._object_models[type(item)] = container_render(
                    render_engine.background_col, render_engine.wall_col)
            else:
                self._object_models[type(item)] = generic_render(
                    render_engine.background_col, style.CBLACK)
        return self._object_models[type(item)].render()

    def render_character(self, pj: InteractiveCharacter): 

        # Check if it is already rendered
        if isinstance(pj, NoPlayerCharacter):
            if pj not in self._object_models:
                self._object_models[pj] = character_render(
                    render_engine.background_col, style.CBLACK)

            weapon = not isinstance(pj.items[BodyParts.HANDS], Staff) if pj.items[BodyParts.HANDS] else None
            self._object_models[pj].update_equipment(
                pj.items[BodyParts.CHEST], pj.items[BodyParts.LEGS], weapon)

        elif isinstance(pj, AnimalCharacter):
            if pj not in self._object_models:
                self._object_models[pj] = animal_render(
                    render_engine.background_col, style.CBLACK)

        
        # Finally update their state and render 
        walking =   isinstance(pj.last_action, Walk)
        attacking = isinstance(pj.last_action, AttackAny)
        beingattacked = isinstance(pj.last_action, BeingAttacked)
        to_east = pj.last_direction == DIRECTIONS[DIRECTION_EAST]
        self._object_models[pj].update_state(
                to_east, walking, attacking, beingattacked, pj.is_dead)
        return self._object_models[pj].render()

    def render_player(self, pj: PlayerCharacter):
        # Extract needed flags
        weapon = not isinstance(pj.items[BodyParts.HANDS], Staff) if pj.items[BodyParts.HANDS] else None
        walking =   isinstance(pj.last_action, Walk)
        attacking = isinstance(pj.last_action, AttackAny)
        beingattacked = isinstance(pj.last_action, BeingAttacked)
        to_east = pj.last_direction == DIRECTIONS[DIRECTION_EAST]

        self._reder_pj.update_equipment(pj.items[BodyParts.CHEST], pj.items[BodyParts.LEGS], weapon)
        self._reder_pj.update_state(to_east, walking, attacking, beingattacked, pj.is_dead)
        return self._reder_pj.render()
