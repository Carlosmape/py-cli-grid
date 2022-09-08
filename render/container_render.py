from .colors import style
from .base_render import base_render


class container_render(base_render):

    def __init__(self, foreground):
        super().__init__(7, 3, foreground)

    def render(self, bg):
        composed_wall = []
        composed_wall.append(self._colorize("  /-\\  ", bg))
        composed_wall.append(self._colorize(" |-x-| ", bg))
        composed_wall.append(self._colorize("  \\-/  ", bg))
        return composed_wall
