from .colors import style
from .base_render import base_render


class generic_render(base_render):

    def __init__(self, foreground, item_bg=style.CBLACKBG):
        super().__init__(7, 3, foreground)
        self._item_bg = item_bg

    def render(self, bg):
        composed_wall = []
        composed_wall.append("   _   ")
        composed_wall.append("  |?|  ")
        composed_wall.append("   ¨   ")
        return self.fill_color(composed_wall, bg)
