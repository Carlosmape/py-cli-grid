from engine.items.interactives.DrinkableItem import AgilityPotion, HealthPotion, DrinkableItem, StrenghtPotion
from .colors import style
from .base_render import base_render


class potion_render(base_render):

    def __init__(self, background, foreground, item: DrinkableItem, item_bg=style.CBLACKBG):
        super().__init__(7, 3, background, foreground)
        self._item_bg = item_bg

        self._filled = style.CVIOLET
        if isinstance(item, AgilityPotion):
            self._filled = style.CYELLOW
        elif isinstance(item, HealthPotion):
            self._filled = style.CRED
        elif isinstance(item, StrenghtPotion):
            self._filled = style.CGREEN

    def render(self):
        composed_wall = []

        common_style = self._back_color+self._fore_color

        # Prepare content of the bottle
        c = self._filled + style.CBOLD + "█" + style.CEND + common_style

        # compose the bottle
        composed_wall.append(common_style + "   ‗   " + style.CEND)
        composed_wall.append(common_style + "   "+c+"   " + style.CEND)
        composed_wall.append(common_style + "       " + style.CEND)
        return composed_wall
