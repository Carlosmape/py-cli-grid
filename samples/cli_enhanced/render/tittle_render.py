from .base_render import base_render
from .colors import style

class tittle_render(base_render):
    # Defined tittle animations
    TITTLE = [
        ['·´·','´·´','·´´','..´','´´.','´¨´'],
    ]

    MAX_STEPS = 6

    def __init__(self, background, foreground):
        super().__init__(7,3, background, foreground)

    def render(self):
        composed_env = []
        if (self._animation_step > tittle_render.MAX_STEPS-1):
            self._animation_step = 0.0
            self._reverse = not self._reverse

        # Calculate current step taking care about reverse animation
        if self._reverse:
            curr_step = tittle_render.MAX_STEPS - 1 - int(self._animation_step)
        else:
            curr_step = int(self._animation_step)

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        if curr_step % 2 == 0:
            composed_env[0] = " PRESS "
            composed_env[1] = "  ANY  "
            composed_env[2] = "  KEY  "

        self._animation_step += 1/(6*tittle_render.MAX_STEPS)
        return self.fill_color(composed_env)
    
    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0,self._frame_height):
            frame[i] = self._back_color+self._fore_color+frame[i] + style.CEND
        return frame
