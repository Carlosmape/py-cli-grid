from random import randint, random
from time import time
from .base_render import base_render
from .colors import style

class env_render(base_render):
    # Defined grass types. Take care about MAX_STEPS
    grass_types = [
        ['·´·','´·´','·´´','..´','´´.','´¨´'],
        [',.,',',,,','.,.','..,','.,.',',,.'],
        ['¨´¨','´¨´','¨´´','¨¨´','´¨´','´´´'],
        [' ´¨','´ ´','¨´ ',' ¨´','´ ´','´´ '],
        [' .,',', ,','., ',' .,','. .',',, '],
        [',. ',',, ','., ',' .,',' ,.',' ,.'],
        [',  ','.  ',' , ',' . ','  .','  ,'],
        ['· ·','´ ´','· ´','. ´','´ .',' ¨´'],
        ['º  ','´  ',' · ',' º ','  ·','  ´'],
        [',ý,','.ŷ,','.ỳ.',',v.',';v.','.ÿ.'],
        [',w,','.ẅ,','.ẃ.',',ŵ.',',ẁ,','.v.']
    ]

    MAX_STEPS = 6

    def __init__(self):
        super().__init__(7,3)
        self.type = randint(0,len(env_render.grass_types)-1)
        self.height_pos = randint(0,self._frame_height-1)
        self._animation_step = env_render.MAX_STEPS * random()

    def render(self):
        composed_env = []
        
        if (self._animation_step > env_render.MAX_STEPS-1):
            self._animation_step = 0.0
            self._reverse = not self._reverse

        # Calculate current step taking care about reverse animation
        if self._reverse:
            curr_step = env_render.MAX_STEPS - 1 - int(self._animation_step)
        else:
            curr_step = int(self._animation_step)

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        composed_env[self.height_pos] = self.get_grass_type(curr_step)

        self._animation_step += 1/(6*env_render.MAX_STEPS)
        return self.fill_color(composed_env)
   
    def get_grass_type(self, step:int):
        """Returns corresponding grass type filled to _frame_width"""
        # Compose the environment element
        return "  " + env_render.grass_types[self.type][step] + "  "
    
    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0,self._frame_height):
            frame[i] = style.CBEIGEBG2+ style.CBEIGE+frame[i] + style.CEND
        return frame
