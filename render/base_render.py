import random
from time import time
from typing import List

from samples.cli_enhanced.ui.graphics.render.colors import style


class base_render():

    def __init__(self, frame_width, frame_height, fore_color: str, step_duration=1.0, max_steps=0, allow_reverse_animation=False):
        # Base animation step
        # Initializes to random to avoid all animations synchronization
        self._animation_step = random.randint(
            0, max_steps-1 if max_steps > 0 else 0)
        self._max_steps = max_steps
        # Animation speed in seconds
        self._step_duration = step_duration
        self._last_step_time = 0
        # Sizing and stuff
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._fore_color = fore_color
        self._allow_reverse = allow_reverse_animation
        self._reverse = False

    def render(self, bg):
        raise NotImplemented

    def fill_color(self, frame: List[str], bg):
        """Fills given frame of size frame_height with background and foreground colors"""
        if len(frame) > self._frame_height:
            raise Exception("Received render model higher than expected")

        for i in range(0, self._frame_height):
            frame[i] = self._colorize(frame[i], bg)

        return frame

    def _colorize(self, string: str, bg):
        """Colorize a string"""
        return bg + self._fore_color + string + style.CEND

    def _fill_frame(self, part: str):
        part_size = len(part)
        return " "*int((self._frame_width - part_size)/2) + part + " "*int(self._frame_width/2)

    def _update_step(self):
        """
        Updates the animation step (taking care about _step_duration)
        Should be called just after render current animation step
        """
        if time() - self._last_step_time > self._step_duration:
            self._last_step_time = time()
            self._animation_step += 1
            if (self._animation_step > self._max_steps-1):
                self._animation_step = 0
                self._reverse = not self._reverse

    def _get_curr_step(self) -> int:
        """
        Calculates current animation step taking care about _allow_reverse flag (to make reverse animations)
        Returned value should be used to render concrete animation step
        """
        if self._allow_reverse and self._reverse:
            return self._max_steps - 1 - self._animation_step
        else:
            return self._animation_step
