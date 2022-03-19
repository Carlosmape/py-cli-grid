from random import randint, random
from time import time
from .base_render import base_render
from .colors import style

class decoration_render(base_render):
    # Defined grass types. Take care about MAX_STEPS
    decoration_types = [
        [',ý,','.ŷ,','.ỳ.',',v.',';v.','.ÿ.'],
        [',w,','.ẅ,','.ẃ.',',ŵ.',',ẁ,','.v.'],
        [',n,','.n,','.n.',',ñ.',',n,','.n.'],
    ]

    MAX_STEPS = 6

    def __init__(self, background, foreground):
        super().__init__(7,3, background, foreground)
        self.type = randint(0,len(decoration_render.decoration_types)-1)
        self.height_pos = randint(0,self._frame_height-1)
        self._animation_step = decoration_render.MAX_STEPS * random()

    def render(self):
        composed_obj = []
        
        if (self._animation_step > decoration_render.MAX_STEPS-1):
            self._animation_step = 0.0
            self._reverse = not self._reverse

        # Calculate current step taking care about reverse animation
        if self._reverse:
            curr_step = decoration_render.MAX_STEPS - 1 - int(self._animation_step)
        else:
            curr_step = int(self._animation_step)

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_obj.append(" "*self._frame_width)

        # Compose the environment element
        composed_obj[self.height_pos] = self.get_grass_type(curr_step)

        self._animation_step += 1/(6*decoration_render.MAX_STEPS)
        return self.fill_color(composed_obj)
   
    def get_grass_type(self, step:int):
        """Returns corresponding grass type filled to _frame_width"""
        # Compose the environment element
        return "  " + decoration_render.decoration_types[self.type][step] + "  "
    
    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0,self._frame_height):
            frame[i] = self._back_color+self._fore_color+frame[i] + style.CEND
        return frame
