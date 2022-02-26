from .base_render import base_render


class item_render(base_render):
    
    def __init__(self):
        super().__init__(7,3)
    
    def render(self):
        composed_wall = []
        composed_wall.append("  /-\\  ")
        composed_wall.append(" |·X·| ")
        composed_wall.append("  \\-/  ")
        return composed_wall

