from .colors import style
from .base_render import base_render


class animal_render(base_render):

    #       ºn'  ºm´  ºn~
    head = ["º", "º", "¤"]
    torso = ["n", "m", "n"]
    tail = ["'", "´", "´"]
    MAX_STEPS = min(len(head), len(torso), len(tail))

    def __init__(self, foreground, item_bg=style.CBLACKBG):
        super().__init__(7, 3, foreground, 1, animal_render.MAX_STEPS, True)
        self._alt_anim = base_render(7, 3, foreground, 0.7, animal_render.MAX_STEPS, True)
        self._act_anim = base_render(7, 3, foreground, 0.2, animal_render.MAX_STEPS, True)
        self._item_bg = item_bg
        self._to_east = True
        self._running = False
        self._attacking = False
        self._beingattacked = False
        self._dead = False

    def update_state(self, to_east, running, attacking, beingattacked,  dead):
        # Update state of the character, should be call just before render new frame
        self._to_east = to_east
        self._running = running
        self._attacking = attacking
        self._beingattacked = beingattacked
        self._dead = dead

    def render(self, bg):
        return self.compose_alive(bg)

    def compose_alive(self, bg):
        composed_animal = []

        head_step = torso_step = self._get_curr_step()
        tail_step = self._alt_anim._get_curr_step()
        if self._running or self._attacking:
            torso_step = tail_step = self._act_anim._get_curr_step()
        if self._attacking:
            head_step = self._act_anim._get_curr_step()

        body = self.compose_animal(head_step, torso_step, tail_step)
        composed_animal.append("       ")
        composed_animal.append("  "+body+"  ")
        composed_animal.append("       ")

        if not self._dead:

            self._update_step()
            self._alt_anim._update_step()
            self._act_anim._update_step()

            if self._beingattacked:
                for i in range(0, self._frame_height):
                    composed_animal[i] = style.CBOLD + composed_animal[i]
            if self._attacking:
                for i in range(0, self._frame_height):
                    composed_animal[i] = style.CITALIC + composed_animal[i]
        return self.fill_color(composed_animal, bg)

    def compose_animal(self, headstep: int, torsostep: int, tailstep: int):
        head = animal_render.head[headstep]
        if self._dead:
            head = "•"
        tors = animal_render.torso[torsostep]
        tail = animal_render.tail[tailstep]

        if self._to_east:
            return tail + tors + head
        else:
            return head + tors + tail
