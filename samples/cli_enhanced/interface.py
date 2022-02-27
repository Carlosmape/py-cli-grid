import os
from time import sleep
from traceback import format_exc
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import Position, Position_types
from engine.frame import Frame
from engine.interface import GUI
from KBHit import KBHit
from engine.menu import Menu
from samples.cli_enhanced.render.colors import style
from samples.cli_enhanced.render.render_engine import render_engine

keyboard = KBHit()
# System call
os.system("")

class CommandLineBox():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []

    def append(self, str_content:str):
        line_size = len(str_content)
        if line_size > self.width:
            raise Exception("CommandLineBox::append: Box width exceeded")
        if len(self.content) < self.height:
            self.content.append(str_content)
        else:
            raise Exception("CommandLineBox::append: Box height exceeded")

class AreaBox(CommandLineBox):
    def __init__(self, width, height, scale_width, scale_height):
        super().__init__(width,height)

        # Calculate scale to draw items
        self.scale_width = scale_width
        self.scale_height = scale_height

        # Items per row and col
        self.objects_per_row = int(self.width/self.scale_width)
        self.objects_per_col = int(self.height/self.scale_height)
        self.objects_in_area = self.objects_per_col*self.objects_per_row
        self.render_engine = render_engine(self.objects_in_area)
        self.from_frame_y = 0
        self.from_frame_x = 0
        self.to_frame_y = 0 
        self.to_frame_x = 0
        self.frame_width = 0
        self.frame_height = 0

        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = int((self.width - self.objects_per_row*self.scale_width)/2)
        self.height_margin = int((self.height - self.objects_per_col*self.scale_height)/2)


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
                            try:
                                items.append(self.render_engine.render_ground((x-self.from_frame_x)*(y-self.from_frame_y)))
                            except:
                                print((x-self.from_frame_x),(y-self.from_frame_y), self.objects_in_area)
                                print(self.from_frame_y,self.to_frame_y,self.from_frame_x, self.to_frame_x)
                                input()

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
        if  frame.player.position.X+self.objects_per_row/2 > frame.area.width:
            desfase_to = frame.player.position.X+self.objects_per_row/2 - frame.area.width

        self.from_frame_x = max(0, int(frame.player.position.X-self.objects_per_row/2-desfase_to))
        self.to_frame_x =   min(frame.area.width+1, int(frame.player.position.X+self.objects_per_row/2+desfase_from))

        self.frame_width = self.to_frame_x - self.from_frame_x
        self.frame_height = self.to_frame_y - self.from_frame_y

        self.width_margin = int((self.width - self.frame_width*self.scale_width)/2)
        self.height_margin = int((self.height - self.frame_height*self.scale_height)/2)

        self.objects_in_area = self.frame_width * self.frame_height

    def get_content_string(self, objects, frame: Frame):
        if not frame.area or not frame.player:
            return
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

        return string +"\n"*self.height_margin+""

class CommandLineInterface(GUI):
    """Enhanced CLI interface for MotorRol"""

    def __init__(self):
        super().__init__()

        # Get terminal size
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines

        # Calculate scale to draw items
        self.scale_width = 7
        self.scale_height = 3

        # Calculate frame sizes for each part
        self.area_container = AreaBox(self.width, self.height/2, self.scale_width, self.scale_height)
        self.status_container = CommandLineBox(self.width, self.height/4)
        self.menu_container = CommandLineBox(self.width, self.height/4)

        # Items per row and col
        self.objects_per_row = int(self.width/self.scale_width)
        self.objects_per_col = int(self.height/self.scale_height)
        self.objects_in_area = self.objects_per_col*self.objects_per_row

        # Initialize Render
        self.render_engine = render_engine(self.objects_in_area)

        #Show start screen before game begins
        self.render_start_screen()

        # Clear console
        self.clear() 

        # Clean user actions
        self.readUserAction();


    def render_start_screen(self):
        # Clear console
        print("height", self.height, "width", self.width)
        print("objects per row:", self.objects_per_row)
        print("objects per col:", self.objects_per_col)
        print("Total objects:",   self.objects_in_area)
        input()
        self.clear() 
        while not self.readUserAction():
            string = str()
            items = []
            for y in range(0, self.objects_per_col+1):
                for x in range(0, self.objects_per_row):
                    items.append(self.render_engine.render_ground(x*y))
                free_spaces = style.CEND + " " * int((self.width - len(items)*self.scale_width)/2)
                str_row = ''
                for i in range(0, self.scale_height):
                    str_row += free_spaces
                    for it in items:
                        str_row += it[i]
                    str_row += free_spaces+"\n"
                string += str_row 
            remain_size = int(self.height - string.count("\n")-1)
            print(string + "\n"*remain_size, end='\r')
            sleep(1/self.max_frame_rate)

    def render(self, frame:Frame):
        str_gui=''

        # Get Area
        composed_area = self.area_container.retrieve_objects(frame)
        if composed_area:
            str_gui += self.area_container.get_content_string(composed_area, frame)

        # Get Menu
        composed_menu = self.render_menu(frame.menu)
        if composed_menu:
            str_gui += composed_menu[0] +"\n"
            str_gui += composed_menu[1] +"\n"
            str_gui += composed_menu[2] +"\n"

        remain_size = int(self.height - str_gui.count("\n")-1)
        print(str_gui+"\n"*remain_size, end='\r')

    
    def render_menu(self, menu:Menu):
        if not menu:
            return
        return self.render_engine.render_menu(menu)

    def readUserAction(self, blocking: bool = False):
        if blocking:
            return input()
        elif keyboard.kbhit():
            return keyboard.getch()

    def doAction(self, action: bytes, player: PlayerCharacter):
        if not self.last_frame:
            return
        elif action == ('w' or 'W'):
            player.move_north(self.last_frame.area)
        elif action == ('a' or 'A'):
            player.move_west(self.last_frame.area)
        elif action == ('s' or 'S'):
            player.move_south(self.last_frame.area)
        elif action == ('d' or 'D'):
            player.move_east(self.last_frame.area)
        elif action == (' '):
            player.active_action_menu(self.last_frame.area)
        elif action and ord(action) == 27:
            player.active_pause_menu()
        #elif action == None:
        #    player.no_move(self.last_frame.area)

    def clear(self):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            os.system('clear')

    def manage_exceptions(self, ex: BaseException):

        # Call super method without return to avoid premature game exit
        super().manage_exceptions(ex)

        # If KeyboardInterrupt do not exit the game
        if isinstance(ex, KeyboardInterrupt):
            return False

        # Show exception info
        else:
            msg = "An error ocurrer during the game\n"
            msg += str(format_exc()) + "\n"
            msg += "Aborting the game execution"
            input(msg)
            return True
