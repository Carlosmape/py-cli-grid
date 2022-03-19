from engine.items.interactives.Potion import Potion
from samples.cli_enhanced.render.colors import style
from .base_render import base_render


class potion_render(base_render):
    
    def __init__(self, background, foreground, item: Potion, item_bg = style.CBLACKBG):
        super().__init__(7,3, background, foreground)
        self._item_bg = item_bg
        
        self._filled = style.CVIOLET
        if item == Potion.Agility():
            self._filled = style.CYELLOW
        elif item == Potion.Health():
            self._filled = style.CRED
        elif item == Potion.Strength():
            self._filled = style.CGREEN

    def render(self):
        composed_wall = []
        
        # Prepare content of the bottle
        c = self._filled + "▄" +self._fore_color

        # compose the bottle
        common_style = self._back_color+self._fore_color
        composed_wall.append(common_style+              "       "+style.CEND)
        composed_wall.append(common_style+style.CBOLD+  "   T   " +style.CEND)
        composed_wall.append(common_style+              "  ("+c+")  "+style.CEND)
        return composed_wall

