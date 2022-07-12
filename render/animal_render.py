from .colors import style
from .base_render import base_render


class animal_render(base_render):

    head = ["º", "º", "º"]
    torso = ["n", "m", "n"]
    tail = ["´", "'", "`"]
    MAX_STEPS = min(len(head), len(torso), len(tail))

    def __init__(self, background, foreground, item_bg=style.CBLACKBG):
        super().__init__(7, 3, background, foreground, 0.5, animal_render.MAX_STEPS, True)
        self._item_bg = item_bg
        self._to_east = True
        self._running = False
        self._attacking = False
        self._dead = False

    def update_state(self, to_east, running, attacking, dead):
        # Update state of the character, should be call just before render new frame
        self._to_east = to_east
        self._running = running
        self._attacking = attacking
        self._dead = dead

    def render(self):

        if self._dead:
            return self.compose_dead()

        composed_animal = []

        curr_step = self._get_curr_step()
        if not self._dead:
            self._update_step()

        body = self.compose_animal(curr_step)

        color = self._back_color+self._fore_color
        composed_animal.append(color+"       "+style.CEND)
        composed_animal.append(color+"  "+body+"  "+style.CEND)
        composed_animal.append(color+"       "+style.CEND)
        return composed_animal

    def compose_dead(self):
        composed_animal = []
        curr_step = self._get_curr_step()
        body = self.compose_animal(curr_step)
        color = self._back_color+self._fore_color+style.CITALIC
        composed_animal.append(color+"       "+style.CEND)
        composed_animal.append(color+"  "+body+"  "+style.CEND)
        composed_animal.append(color+"       "+style.CEND)
        return composed_animal



    def compose_animal(self, step: int):
        head = animal_render.head[step]
        tors = animal_render.torso[step]
        tail = animal_render.tail[step]

        if self._to_east:
            return tail + tors + head
        else:
            return head + tors + tail
