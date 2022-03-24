from random import randint, random
from time import time
from .base_render import base_render
from .colors import style

class env_render(base_render):
    # Defined grass types. Take care about MAX_STEPS
    TYPES = [
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

    MAX_STEPS = len(TYPES[0])

    def __init__(self, background, foreground):
        super().__init__(7,3, background, foreground, 0.5, env_render.MAX_STEPS, True)
        self.type = randint(0,len(env_render.TYPES)-1)
        self.height_pos = randint(0,self._frame_height-1)

    def render(self):
        composed_env = []
        
        # Calculate current step taking care about reverse animation
        curr_step = self._get_curr_step()

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        composed_env[self.height_pos] = self.get_grass_type(curr_step)
        
        self._update_step()

        return self.fill_color(composed_env)
   
    def get_grass_type(self, step:int):
        """Returns corresponding grass type filled to _frame_width"""
        # Compose the environment element
        return "  " + env_render.TYPES[self.type][step] + "  "
    
    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0,self._frame_height):
            frame[i] = self._back_color+self._fore_color+frame[i] + style.CEND
        return frame
