from random import randint
from .base_render import base_render


class GrassRender(base_render):
    # Defined grass types. Take care about MAX_STEPS
    TYPES = [
        ['   ', '   ', '   ', '   ', '   ', '   '],
        [' ´ ', ' · ', ' ´ ', ' . ', ' ´ ', ' ¨ '],
        ['·´·', '´·´', '·´´', '..´', '´´.', '´¨´'],
        [',.,', ',,,', '.,.', '..,', '.,.', ',,.'],
        ['¨´¨', '´¨´', '¨´´', '¨¨´', '´¨´', '´´´'],
        [' ´¨', '´ ´', '¨´ ', ' ¨´', '´ ´', '´´ '],
        [' .,', ', ,', '., ', ' .,', '. .', ',, '],
        [',. ', ',, ', '., ', ' .,', ' ,.', ' ,.'],
        [',  ', '.  ', ' , ', ' . ', '  .', '  ,'],
        ['· ·', '´ ´', '· ´', '. ´', '´ .', ' ¨´'],
        ['º  ', '´  ', ' · ', ' º ', '  ·', '  ´'],
        [',ý,', '.ŷ,', '.ỳ.', ',v.', ';v.', '.ÿ.'],
        [',w,', '.ẅ,', '.ẃ.', ',ŵ.', ',ẁ,', '.v.']
    ]

    MAX_STEPS = len(TYPES[0])

    def __init__(self, foreground):
        super().__init__(7, 3, foreground, 0.5, GrassRender.MAX_STEPS, True)
        self.type = randint(0, len(GrassRender.TYPES)-1)
        self.height_pos = randint(0, self._frame_height-1)

    def render(self, bg):
        composed_env = []

        # Calculate current step taking care about reverse animation
        curr_step = self._get_curr_step()

        # Fill 3x5 frame with empty spaces
        for i in range(0, self._frame_height):
            composed_env.append(" "*self._frame_width)

        # Compose the environment element
        composed_env[self.height_pos] = self.get_grass_type(curr_step)

        self._update_step()

        return self.fill_color(composed_env, bg)

    def get_grass_type(self, step: int):
        """Returns corresponding grass type filled to _frame_width"""
        # Compose the environment element
        return "  " + GrassRender.TYPES[self.type][step] + "  "
