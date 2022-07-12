from .colors import style
from .base_render import base_render


class wall_render(base_render):

    WALL = [
        style.CGREYBG + style.CWHITE2 + "¯¦¯¯¦¯¯" + style.CEND,
        style.CGREYBG + style.CWHITE2 + "¯¯¦¯¯¯¦" + style.CEND,
        style.CGREYBG + style.CWHITE2 + "¦¯¯¦¯¯¯" + style.CEND,
    ]
    def __init__(self, background, foreground):
        super().__init__(7, 3, background, foreground)

    def render(self):
        return wall_render.WALL
