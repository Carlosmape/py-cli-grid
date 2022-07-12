from .colors import style
from .base_render import base_render


class rock_render(base_render):

    def __init__(self, background, foreground):
        super().__init__(7, 3, background, foreground)

    def render(self):
        composed_wall = []
        for i in range(self._frame_height):
            # Compose each item row
            # if i % 2 == 0:
            #    row = "▓"*i+"█"*(self._frame_width-i)
            # else:
            #    row = "█"*(self._frame_width-i)+"▓"*i
            row = "█"*self._frame_width
            composed_wall.append(
                self._back_color+self._fore_color+row + style.CEND)
        return composed_wall
