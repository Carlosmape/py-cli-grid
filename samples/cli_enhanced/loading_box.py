from random import randint
from engine.characters.Base import DIRECTION_EAST, DIRECTION_WEST, DIRECTIONS
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.items.interactives.WearableItem import HandsWearable
from samples.cli_enhanced.area_box import AreaBox
from samples.cli_enhanced.command_line_box import CommandLineBox


class LoadingBox(AreaBox):
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height,scale_width, scale_height)
        self.loaded = False
        self.width_margin = int((self.width - (self.max_obj_in_width)*self.scale_width)/2)
        self.height_margin = int((self.height - (self.max_obj_in_height)*self.scale_height)/2)
        self.map_width = self.max_obj_in_width 
        self.map_height = self.max_obj_in_height
        self.tittle_box = CommandLineBox(width, height/5)
        self.npcs = []
        for i in range(4):
            self.npcs.append(NoPlayerCharacter(Position(self.max_obj_in_height/2,self.max_obj_in_width/2),1))
            self.npcs[i].items[BodyParts.hands] = HandsWearable.Any()

    def _update_npcs(self):
        for npc in self.npcs:
            action = randint(0,50)
            if action == 0:
                npc.is_moving = not npc.is_moving
            elif action == 1:
                npc.last_direction = DIRECTIONS[DIRECTION_WEST]
            elif action == 2:
                npc.last_direction = DIRECTIONS[DIRECTION_EAST]
            elif action == 3:
                npc.is_moving = False

    def _extract_objects(self):
        self._update_npcs()
        items = []
        for y in range(0, self.max_obj_in_height):
            for x in range(0, self.max_obj_in_width):
                if y == self.max_obj_in_height/2 and x == self.max_obj_in_width/2:
                    items.append(self.render_engine.render_tittle(self.loaded))
                elif y-2 == self.max_obj_in_height/2 and x-2 == self.max_obj_in_width/2:
                    items.append(self.render_engine.render_character(self.npcs[0]))
                elif y+2 == self.max_obj_in_height/2 and x-2 == self.max_obj_in_width/2:
                    items.append(self.render_engine.render_character(self.npcs[1]))
                elif y-2 == self.max_obj_in_height/2 and x+2 == self.max_obj_in_width/2:
                    items.append(self.render_engine.render_character(self.npcs[2]))
                elif y+2 == self.max_obj_in_height/2 and x+2 == self.max_obj_in_width/2:
                    items.append(self.render_engine.render_character(self.npcs[3]))               
                else:
                    items.append(self.render_engine.render_ground(x*y))

        return items
   
    def complete_load(self):
        self.loaded = True

    def render(self):
        obj = self._extract_objects()
        return self._compose_frame_string(obj)
