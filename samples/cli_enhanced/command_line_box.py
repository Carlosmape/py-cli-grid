
from random import randint
from engine.characters.Base import DIRECTION_EAST, DIRECTION_WEST, DIRECTIONS
from engine.characters.NoPlayerCharacter import NoPlayerCharacter
from engine.defines.defines import BodyParts, Position
from engine.frame import Frame
from engine.items.interactives.WearableItem import HandsWearable, WearableItem
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.render.render_engine import render_engine


class CommandLineBox():
    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height
    
    def _fill_box(self, string):
        self.height_margin = int(self.height - string.count("\n"))
        return string +"\n"*self.height_margin+""

    def render(self, string:str):
        return self._fill_box(string)

class AreaBox(CommandLineBox):
    """This CommandLineBox works specially to contain the Frame Area"""
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height)

        # Scale area map to screen
        self.scale_width = scale_width
        self.scale_height = scale_height

        # Items per row and col
        self.max_obj_in_width = int(self.width/self.scale_width)
        self.max_obj_in_height = int(self.height/self.scale_height)
        self.max_objects_in_area =(self.max_obj_in_height)*(self.max_obj_in_width)

        #Models engine
        self.render_engine = render_engine(self.max_objects_in_area)

        # Frame drawing
        self.obj_in_map = self.max_objects_in_area
        self.map_from_y = 0
        self.map_from_x = 0
        self.map_to_y = 0 
        self.map_to_x = 0
        self.map_width = 0
        self.map_height = 0

        # Margin spaces to fill drawed frame to entire area
        self.width_margin = int((self.width - self.max_obj_in_width*self.scale_width)/2)
        self.height_margin = int((self.height - self.max_obj_in_height*self.scale_height)/2)

    def _fill_box(self, string):
        return string +"\n"*self.height_margin+""

    def _extract_objects(self, frame: Frame):
        items = []
        
        self._update_frame_size(frame)

        for y in range(self.map_from_y, self.map_to_y):
            for x in range(self.map_from_x, self.map_to_x):
                current_pos = Position(x,y)
                if frame.player.position == current_pos:
                    items.append(self.render_engine.render_player(frame.player))
                else:
                    npc = frame.get_npc(current_pos)
                    if npc:
                        items.append(self.render_engine.render_character(npc))
                    else:
                        item = frame.area.item(current_pos)
                        if item:
                            items.append(self.render_engine.render_item(item))
                        else:
                            items.append(self.render_engine.render_ground((x*y)%self.max_objects_in_area))

        return items

    def _update_frame_size(self, frame: Frame):
        #Calculate frame of the area to render
        pj = frame.player.position

        # Calculate desfases (when the pj is in the map edges, 
        # remaining elements shall drawed in the oposite side)
        desfase_from = 0
        if pj.Y-self.max_obj_in_height/2 < 0:
            desfase_from = self.max_obj_in_height + (pj.Y-self.max_obj_in_height/2)

        desfase_to = 0
        if  pj.Y+self.max_obj_in_height/2 > frame.area.height+1:
            desfase_to = pj.Y+self.max_obj_in_height/2 - frame.area.height+1

        self.map_from_y = max(0, int(pj.Y-self.max_obj_in_height/2-desfase_to))
        self.map_to_y =   min(frame.area.height+1, int(pj.Y+self.max_obj_in_height/2+desfase_from))

        desfase_from = 0
        if pj.X-self.max_obj_in_width/2 < 0:
            desfase_from = self.max_obj_in_width - pj.X-self.max_obj_in_width/2 

        desfase_to = 0
        if pj.X+self.max_obj_in_width/2 > frame.area.width+1:
            desfase_to = pj.X+self.max_obj_in_width/2 - frame.area.width+1

        self.map_from_x = max(0, int(pj.X-self.max_obj_in_width/2-desfase_to))
        self.map_to_x =   min(frame.area.width+1, int(pj.X+self.max_obj_in_width/2+desfase_from))

        self.map_width = self.map_to_x - self.map_from_x
        self.map_height = self.map_to_y - self.map_from_y

        self.width_margin = int((self.width - self.map_width*self.scale_width)/2)
        self.height_margin = int((self.height - self.map_height*self.scale_height)/2)

        self.obj_in_map = self.map_width * self.map_height

    def _compose_frame_string(self, objects):
        if len(objects) != self.obj_in_map:
            raise Exception("AreaBox::_compose_frame_string: Received unexpected objects number %d/%d"%(len(objects),self.obj_in_map))

        string = "\n"*self.height_margin
        free_spaces = style.CEND + " " * self.width_margin

        for y in reversed(range(0, self.map_height)):
            items = objects[y*self.map_width:(y*self.map_width+self.map_width)]

            #draw this row of objects
            str_row = ''
            for i in range(0, self.scale_height):
                str_row += free_spaces
                for it in items:
                    str_row += it[i]
                str_row += free_spaces + "\n"
            string += str_row 

        return self._fill_box(string)

    def render(self, frame: Frame):
        if not frame.area or not frame.player:
            return ""
        frame_objects = self._extract_objects(frame)
        return self._compose_frame_string(frame_objects)

class LoadingBox(AreaBox):
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height,scale_width, scale_height)
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
                    items.append(self.render_engine.render_tittle())
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
   
    def render(self):
        obj = self._extract_objects()
        return self._compose_frame_string(obj)
