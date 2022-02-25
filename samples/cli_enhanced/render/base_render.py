class base_render():

    def __init__(self, frame_width, frame_height):
        # Base animation step (when iddle)
        self._animation_step = 0.0
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._reverse = False
    
    def render(self):
        raise NotImplemented

    def _fill_frame(self, part:str):
        part_size = len(part)
        return " "*int((self._frame_width - part_size)/2) + part + " "*int(self._frame_width/2)


