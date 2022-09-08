from .base_render import base_render
from .colors import style


class tittle_render(base_render):
    # Defined tittle animations
    LOAD = ['[-]', '[\]', '[|]', '[/]', '[-]', '[\]', '[|]', '[/]']

    MAX_STEPS = len(LOAD)

    def __init__(self, foreground):
        super().__init__(7, 3, foreground, 0.2, tittle_render.MAX_STEPS, False)

    def render(self, loaded, bg):
        composed_env = []
        curr_step = self._get_curr_step()
        self._update_step()
        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        if loaded:
            if curr_step % 2 == 0:
                composed_env[0] = style.CBOLD + " PRESS "
                composed_env[1] = style.CBOLD + " -ANY- "
                composed_env[2] = style.CBOLD + "  KEY  "
        else:
            composed_env[0] = style.CBOLD + "GAME IS"
            composed_env[1] = style.CBOLD + "  "+tittle_render.LOAD[curr_step]+"  "
            composed_env[2] = style.CBOLD + "LOADING"

        return self.fill_color(composed_env, bg)
