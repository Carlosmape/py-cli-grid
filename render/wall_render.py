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
        rendered = []
        rendered.append(self._colorize(wall_render.WALL[0], style.CGREYBG))
        rendered.append(self._colorize(wall_render.WALL[1], style.CGREYBG))
        rendered.append(self._colorize(wall_render.WALL[2], style.CGREYBG))
        return rendered
