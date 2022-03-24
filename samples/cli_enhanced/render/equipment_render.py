from engine.items.interactives.WearableItem import ChestWearable, FeetsWearable, HandsWearable, WearableItem
from samples.cli_enhanced.render.colors import style
from .base_render import base_render


class equipment_render(base_render):
    # Define equipment models
    FeetsObject = [
            "       ",
            "       ",
            "   db  "
            ]
    HeadObect = [
            "       ",
            "   _   ",
            "  (ö)  ",
            ]
    WeaponObject = [ 
                        "       ",
            style.CBOLD+"   ┼   ",
            style.CBOLD+"  -┴-  ",
            ]
    ChestObject = [
            "       ",
            "       ",
            "  î#î  ",
            ]
    
    def __init__(self, background, foreground, item:WearableItem, item_bg = style.CBLACKBG):
        super().__init__(7,3, background, foreground)
        self._item_bg = item_bg
        if isinstance(item, FeetsWearable):
            self.obj = equipment_render.FeetsObject
        elif isinstance(item, HandsWearable):
            self.obj = equipment_render.WeaponObject
        elif isinstance(item, ChestWearable):
            self.obj = equipment_render.ChestObject
        else:
            self.obj = equipment_render.HeadObect
    
    def render(self):
        return [ 
            self._back_color+self._fore_color+self.obj[0]+style.CEND,
            self._back_color+self._fore_color+self.obj[1]+style.CEND,
            self._back_color+self._fore_color+self.obj[2]+style.CEND,
                ]

