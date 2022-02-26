from .base_render import base_render


class wall_render(base_render):
    
    def __init__(self):
        super().__init__(7,3)
    
    def render(self):
        composed_wall = []
        composed_wall.append("XXXXXXX")
        composed_wall.append("XXXXXXX")
        composed_wall.append("XXXXXXX")
        return composed_wall

