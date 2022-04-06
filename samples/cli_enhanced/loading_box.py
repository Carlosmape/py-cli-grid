from engine.characters.AnimalCharacter import AnimalCharacter
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.items.interactives.WearableItem import HandsWearable
from engine.world.area import area
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
        self.area = area(1)
        self.npcs = []
        for i in range(int(self.max_objects_in_area/10)):
            if i % 3 == 0:
                self.npcs.append(AnimalCharacter(None, 1, self.area.generate_empty_position(False)))
            else:
                self.npcs.append(NoPlayerCharacter(None, 1, self.area.generate_empty_position(False)))
                self.npcs[i].items[BodyParts.hands] = HandsWearable.Any()
            self.npcs[i].area = self.area

    def _update_npcs(self):
        for npc in self.npcs:
            npc.Move()

    def _extract_objects(self):
        self._update_npcs()

        items = []
        middle_height = int(self.max_obj_in_height/2)
        middle_width = int(self.max_obj_in_width/2)

        for y in range(0, self.max_obj_in_height):
            for x in range(0, self.max_obj_in_width):

                # Draw ground by default
                it = self.render_engine.render_ground(x*y)

                # Or corresponding element
                if y == middle_height and x == middle_width:
                    it = self.render_engine.render_tittle(self.loaded)
                elif Position(x,y) in self.area.items:
                    it = self.render_engine.render_item(self.area.item(Position(x,y)))
                else:
                    for npc in self.npcs:
                        if Position(x, y) == npc.position:
                            it = self.render_engine.render_character(npc)

                items.append(it)

        return items
   
    def complete_load(self):
        self.loaded = True

    def render(self):
        obj = self._extract_objects()
        return self._compose_frame_string(obj)
