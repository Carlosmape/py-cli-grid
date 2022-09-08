from .colors import style
from .base_render import base_render


class wood_wall_render(base_render):

    WALL = [
        "¯¯¯¯¯¯¦",
        "¯¯¯¦¯¯¯",
        "¦¯¯¯¯¯¯",
    ]
    def __init__(self):
        super().__init__(7, 3, style.CYELLOW2)

    def render(self):
        return self.fill_color(wood_wall_render.WALL, style.CYELLOWBG)
