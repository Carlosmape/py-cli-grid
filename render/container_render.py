from .colors import style
from .base_render import base_render


class container_render(base_render):

    def __init__(self, background, foreground):
        super().__init__(7, 3, background, foreground)

    def render(self):
        composed_wall = []
        composed_wall.append(self._colorize("  /-\\  "))
        composed_wall.append(self._colorize(" |-x-| "))
        composed_wall.append(self._colorize("  \\-/  "))
        return composed_wall
