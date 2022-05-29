from random import randint
from .base_render import base_render
from .colors import style


class decoration_render(base_render):
    # Defined grass types. Take care about MAX_STEPS
    TYPES = [
        [',ý,', '.ŷ,', '.ỳ.', ',v.', ';v.', '.ÿ.'],
        [',w,', '.ẅ,', '.ẃ.', ',ŵ.', ',ẁ,', '.v.'],
        [',n,', '.n,', '.n.', ',ñ.', ',n,', '.n.'],
    ]

    MAX_STEPS = len(TYPES[0])

    def __init__(self, background, foreground):
        super().__init__(7, 3, background, foreground, 1, decoration_render.MAX_STEPS, True)
        self.type = randint(0, len(decoration_render.TYPES)-1)
        self.height_pos = randint(0, self._frame_height-1)

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
            frame[i] = self._back_color+self._fore_color+frame[i] + style.CEND
        return frame
