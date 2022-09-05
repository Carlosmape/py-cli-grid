from random import randint

from engine.items.interactives.CollectibleItem import DecorationItem
from samples.assets.items.collectibles import Feather, Leaves, Rock, Stick
from .base_render import base_render
from .colors import style


class decoration_render(base_render):
    """Represents collectible-non edible engine objects (sticks, rocks)"""

    # Defined grass types. Take care about MAX_STEPS
    # (all elements shall be the same length)
    TYPES = [
        # GENERIC
        [',n,', '.n,', '.n.', ',ñ.', ',n,', '.n.'],
        # ROCKS
        [',o,', '.o,', '.o.', ',o.', ',o,', '.o.'],
        # STICKS
        [',ƒ,', '.ƒ,', '.ƒ.', ',ƒ.', ',ƒ,', '.ƒ.'],
        # LEAVES
        [',-,', '..,', '.,.', ',..', ',.,', '.-.'],
        # FEATHER
        [',ð,', '.ð,', '.ð.', ',ð.', ',ð,', '.ð.'],
        # MOSS
        [',m,', '.m,', '.m.', ',m.', ',m,', '.m.'],
    ]

    MAX_STEPS = len(TYPES[0])

    def __init__(self, background, foreground, item: DecorationItem):
        super().__init__(7, 3, background, foreground, 1, decoration_render.MAX_STEPS, True)
        self.height_pos = randint(0, self._frame_height-1)

        # Select rendering type depending on collectible item type
        self.type = 0
        if isinstance(item, Rock):
            self.type = 0
        elif isinstance(item, Stick):
            self.type = 2
        elif isinstance(item, Leaves):
            self.type = 3
        elif isinstance(item, Feather):
            self.type = 4

    def render(self):
        composed_obj = []

        curr_step = self._get_curr_step()

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_obj.append(" "*self._frame_width)

        # Compose the environment element
        composed_obj[self.height_pos] = self.get_grass_type(curr_step)

        self._update_step()
        return self.fill_color(composed_obj)

    def get_grass_type(self, step: int):
        """Returns corresponding grass type filled to _frame_width"""
        # Compose the environment element
        return "  " + decoration_render.TYPES[self.type][step] + "  "

    def fill_color(self, frame):
        """Fills frame with background and colors the grass elements"""
        for i in range(0, self._frame_height):
            frame[i] = self._colorize(frame[i])
        return frame
