from .base_render import base_render
from .colors import style

class tittle_render(base_render):
    # Defined tittle animations
    LOAD = ['[-]','[\]','[|]','[/]','[-]','[\]','[|]','[/]']

    MAX_STEPS = len(LOAD)

    def __init__(self, background, foreground):
        super().__init__(7,3, background, foreground)

    def render(self, loaded = False):
        composed_env = []
        if (self._animation_step > tittle_render.MAX_STEPS-1):
            self._animation_step = 0.0

        # Calculate current step taking care about reverse animation
        curr_step = int(self._animation_step)

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        if loaded:
            if curr_step % 2 == 0:
                composed_env[0] = " PRESS "
                composed_env[1] = "  ANY  "
                composed_env[2] = "  KEY  "
            self._animation_step += 1/(4*tittle_render.MAX_STEPS)
        else:
            composed_env[0] = "LOADING"
            composed_env[1] = "  "+tittle_render.LOAD[curr_step]+"  "
            composed_env[2] = " GAME  "
            self._animation_step += 1/(2)

        return self.fill_color(composed_env)
    
    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0,self._frame_height):
            frame[i] = self._back_color+style.CBOLD+self._fore_color+frame[i] + style.CEND
        return frame
