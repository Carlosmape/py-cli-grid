from samples.cli_enhanced.render.colors import style
from .base_render import base_render


class item_render(base_render):
    
    def __init__(self, background, foreground, item_bg = style.CBLACKBG):
        super().__init__(7,3, background, foreground)
        self._item_bg = item_bg
    
    def render(self):
        composed_wall = []
        composed_wall.append(self._back_color+self._fore_color+"   _   "+style.CEND)
        composed_wall.append(self._back_color+self._fore_color+"  |x|  " +style.CEND)
        composed_wall.append(self._back_color+self._fore_color+"   ¨   "+style.CEND)
        return composed_wall

