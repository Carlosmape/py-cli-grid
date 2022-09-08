from engine.items.interactives.WearableItem import BackWearable, ChestWearable, FeetsWearable, HandsWearable, LegsWearable, ShoulderWearable, WearableItem
from .colors import style
from .base_render import base_render


class equipment_render(base_render):
    # Define equipment models
    HeadObject = [
        "       ",
        "  _n_  ",
        "       ",
    ]
    ShoudlerObject = [
        "       ",
        "       ",
        "  ^-^  "
    ]
    BackObject = [
        "   _   ",
        "  (º)  ",
        "   ¨   ",
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
    LegsObject = [
        "       ",
        "       ",
        "  /|\\  "
    ]
    FeetsObject = [
        "       ",
        "       ",
        "   db  "
    ]

    def __init__(self, foreground, item: WearableItem, item_bg=style.CBLACKBG):
        super().__init__(7, 3, foreground)
        self._item_bg = item_bg
        if isinstance(item, FeetsWearable):
            self.obj = equipment_render.FeetsObject
        elif isinstance(item, HandsWearable):
            self.obj = equipment_render.WeaponObject
        elif isinstance(item, ChestWearable):
            self.obj = equipment_render.ChestObject
        elif isinstance(item, ShoulderWearable):
            self.obj = equipment_render.ShoudlerObject
        elif isinstance(item, LegsWearable):
            self.obj = equipment_render.LegsObject
        elif isinstance(item, BackWearable):
            self.obj = equipment_render.BackObject
        else:
            self.obj = equipment_render.HeadObject

    def render(self, bg):
        return self.fill_color(self.obj, bg)
