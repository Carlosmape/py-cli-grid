from samples.cli_enhanced.render.colors import style
from .base_render import base_render


class wall_render(base_render):
    
    def __init__(self, background, foreground):
        super().__init__(7,3, background, foreground)
    
    def render(self):
        composed_wall = []
        for i in range(self._frame_height):
            composed_wall.append(self._back_color+self._fore_color+"█"*self._frame_width + style.CEND)
        return composed_wall

