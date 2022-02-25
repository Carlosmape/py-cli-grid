from random import randint
from time import time
from base_render import base_render

class env_render(base_render):
    
    grass0 =  ['·´·', '´·´', '·´´']
    grass1 =  [',.,', ',,,', '.,.']
    grass2 =  ['¨´¨', '´¨´','¨´´']

    flower0 =  [',ý,', '.ÿ,', '.v.']
    flower1 =  [',w,', '.ẅ,', '.ẃ.']

    MAX_STEPS = 3

    def __init__(self, flower = True):
        super().__init__(3,1)
        self.is_flower = flower
        if not flower:
            self.type = randint(0,2)
        else:
            self.type = randint(0,1)

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
        
        # Compose the environment element
        if self.is_flower:
            if self.type == 0:
                composed_env.append(self._fill_frame(env_render.flower0[curr_step]))
            else:
                composed_env.append(self._fill_frame(env_render.flower1[curr_step]))
        else:
            if self.type == 0:
                composed_env.append(self._fill_frame(env_render.grass0[curr_step]))
            elif self.type == 1:
                composed_env.append(self._fill_frame(env_render.grass1[curr_step]))
            else:
                composed_env.append(self._fill_frame(env_render.grass2[curr_step]))

        self._animation_step += 1/(2*env_render.MAX_STEPS)
        return composed_env

