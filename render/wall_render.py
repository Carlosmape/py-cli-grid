from .colors import style
from .base_render import base_render


class wall_render(base_render):

    WALL = [
        "¯¦¯¯¦¯¯",
        "¯¯¦¯¯¯¦",
        "¦¯¯¦¯¯¯",
    ]
    def __init__(self):
        super().__init__(7, 3, style.CWHITE2)

    def render(self):
        return self.fill_color(wall_render.WALL, style.CGREYBG)
