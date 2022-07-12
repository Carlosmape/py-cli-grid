from .colors import style
from .base_render import base_render


class generic_render(base_render):

    def __init__(self, background, foreground, item_bg=style.CBLACKBG):
        super().__init__(7, 3, background, foreground)
        self._item_bg = item_bg

    def render(self):
        composed_wall = []
        composed_wall.append(self._colorize("   _   "))
        composed_wall.append(self._colorize("  |?|  "))
        composed_wall.append(self._colorize("   ¨   "))
        return composed_wall
