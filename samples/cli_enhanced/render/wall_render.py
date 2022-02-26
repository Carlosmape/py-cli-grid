from .base_render import base_render


class wall_render(base_render):
    
    def __init__(self):
        super().__init__(7,3)
    
    def render(self):
        composed_wall = []
        for i in range(self._frame_height):
            composed_wall.append("█"*self._frame_width)
        return composed_wall
