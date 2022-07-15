from .base_render import base_render
from .colors import style


class tittle_render(base_render):
    # Defined tittle animations
    LOAD = ['[-]', '[\]', '[|]', '[/]', '[-]', '[\]', '[|]', '[/]']

    MAX_STEPS = len(LOAD)

    def __init__(self, background, foreground):
        super().__init__(7, 3, background, foreground, 0.2, tittle_render.MAX_STEPS, False)

    def render(self, loaded=False):
        composed_env = []
        curr_step = self._get_curr_step()
        self._update_step()
        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        if loaded:
            if curr_step % 2 == 0:
                composed_env[0] = " PRESS "
                composed_env[1] = " -ANY- "
                composed_env[2] = "  KEY  "
        else:
            composed_env[0] = "GAME IS"
            composed_env[1] = "  "+tittle_render.LOAD[curr_step]+"  "
            composed_env[2] = "LOADING"

        return self.fill_color(composed_env)

    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0, self._frame_height):
            frame[i] = self._colorize(style.CBOLD + frame[i])
        return frame
