
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
    
    def fill_box(self, string):
        self.height_margin = int(self.height - string.count("\n"))
        return string +"\n"*self.height_margin+""

class AreaBox(CommandLineBox):
    """This CommandLineBox works specially to contain the Frame Area"""
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height)

        # Calculate scale to draw items
        self.scale_width = scale_width
        self.scale_height = scale_height

        # Items per row and col
        self.objects_per_row = int(self.width/self.scale_width)
        self.objects_per_col = int(self.height/self.scale_height)
        self.objects_in_area = (self.objects_per_col)*(self.objects_per_row)
        self.max_objects_in_area = self.objects_in_area
        self.render_engine = render_engine(self.max_objects_in_area)
        self.from_frame_y = 0
        self.from_frame_x = 0
        self.to_frame_y = 0 
        self.to_frame_x = 0
        self.frame_width = 0
        self.frame_height = 0

        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = int((self.width - self.objects_per_row*self.scale_width)/2)
        self.height_margin = int((self.height - self.objects_per_col*self.scale_height)/2)

    def fill_box(self, string):
        return string +"\n"*self.height_margin+""

    def retrieve_objects(self, frame: Frame):
        if not frame.area or not frame.player:
            return
        items = []
        
        self.update_frame_sizes(frame)

        for y in range(self.from_frame_y, self.to_frame_y):
            for x in range(self.from_frame_x, self.to_frame_x):
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

    def update_frame_sizes(self, frame: Frame):
        #Calculate frame of the area to render
        desfase_from = 0
        if int(frame.player.position.Y-self.objects_per_col/2) < 0:
            desfase_from = self.objects_per_col + (frame.player.position.Y-self.objects_per_col/2)
        else:
            desfase_from = 0
        desfase_to = 0
        if  int(frame.player.position.Y+self.objects_per_col/2) > frame.area.height+1:
            desfase_to = int(frame.player.position.Y+self.objects_per_col/2) - frame.area.height+1
        else:
            desfase_to = 0
        self.from_frame_y = max(0, int(frame.player.position.Y-self.objects_per_col/2-desfase_to))
        self.to_frame_y =   min(frame.area.height+1, int(frame.player.position.Y+self.objects_per_col/2+desfase_from))

        desfase_from = 0
        if frame.player.position.X-self.objects_per_row/2 < 0:
            desfase_from = self.objects_per_row - frame.player.position.X-self.objects_per_row/2 

        desfase_to = 0
        if  frame.player.position.X+self.objects_per_row/2 > frame.area.width+1:
            desfase_to = frame.player.position.X+self.objects_per_row/2 - frame.area.width+1

        self.from_frame_x = max(0, int(frame.player.position.X-self.objects_per_row/2-desfase_to))
        self.to_frame_x =   min(frame.area.width+1, int(frame.player.position.X+self.objects_per_row/2+desfase_from))

        self.frame_width = self.to_frame_x - self.from_frame_x
        self.frame_height = self.to_frame_y - self.from_frame_y

        self.width_margin = int((self.width - self.frame_width*self.scale_width)/2)
        self.height_margin = int((self.height - self.frame_height*self.scale_height)/2)

        self.objects_in_area = self.frame_width * self.frame_height

    def get_content_string(self, objects):

        if len(objects) != self.objects_in_area:
            raise Exception("AreaBox::get_content_string: Received unexpected objects number %d/%d"%(len(objects),self.objects_in_area))

        string = "\n"*self.height_margin
        free_spaces = style.CEND + " " * self.width_margin

        for y in reversed(range(0, self.frame_height)):
            items = objects[y*self.frame_width:(y*self.frame_width+self.frame_width)]

            #draw this row of objects
            str_row = ''
            for i in range(0, self.scale_height):
                str_row += free_spaces
                for it in items:
                    str_row += it[i]
                str_row += free_spaces + "\n"
            string += str_row 
        return self.fill_box(string)

class LoadingBox(AreaBox):
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height,scale_width, scale_height)
        self.width_margin = int((self.width - (self.objects_per_row)*self.scale_width)/2)
        self.height_margin = int((self.height - (self.objects_per_col)*self.scale_height)/2)
        self.frame_width = self.objects_per_row 
        self.frame_height = self.objects_per_col
        self.npcs = []
        for i in range(4):
            self.npcs.append(NoPlayerCharacter(Position(self.objects_per_col/2,self.objects_per_row/2),1))
            self.npcs[i].items[BodyParts.hands] = HandsWearable.Any()

    def update_dummys_npc(self):
        for npc in self.npcs:
            action = randint(0,3)
            if action == 0:
                npc.is_moving = not npc.is_moving
            elif action == 1:
                npc.last_direction = DIRECTIONS[DIRECTION_WEST]
            elif action == 2:
                npc.last_direction = DIRECTIONS[DIRECTION_EAST]
            elif action == 3:
                npc.is_moving = False

    def retrieve_objects(self):
        self.update_dummys_npc()
        items = []
        for y in range(0, self.objects_per_col):
            for x in range(0, self.objects_per_row):
                if y == self.objects_per_col/2 and x == self.objects_per_row/2:
                    items.append(self.render_engine.render_tittle())
                elif y-2 == self.objects_per_col/2 and x-2 == self.objects_per_row/2:
                    items.append(self.render_engine.render_character(self.npcs[0]))
                elif y+2 == self.objects_per_col/2 and x-2 == self.objects_per_row/2:
                    items.append(self.render_engine.render_character(self.npcs[1]))
                elif y-2 == self.objects_per_col/2 and x+2 == self.objects_per_row/2:
                    items.append(self.render_engine.render_character(self.npcs[2]))
                elif y+2 == self.objects_per_col/2 and x+2 == self.objects_per_row/2:
                    items.append(self.render_engine.render_character(self.npcs[3]))               
                else:
                    items.append(self.render_engine.render_ground(x*y))

        return items

