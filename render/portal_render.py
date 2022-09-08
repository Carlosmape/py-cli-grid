from .colors import style
from .base_render import base_render


class portal_render(base_render):

    def __init__(self, foreground):
        super().__init__(7, 3, foreground)

    def render(self, bg):
        composed_wall = []
        composed_wall.append(" "+self._colorize(style.CBOLD+"┼┼┼┼┼", bg)+" ")
        composed_wall.append(" "+self._colorize(style.CBOLD+"┼┼┼O┼", bg)+" ")
        composed_wall.append(" "+self._colorize(style.CBOLD+"┼┼┼┼┼", bg)+" ")
        return composed_wall
