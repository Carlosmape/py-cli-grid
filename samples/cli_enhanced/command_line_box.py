
import re


class CommandLineBox():
    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height
    
    def _fill_box(self, string):
        self.height_margin = int(self.height - string.count("\n"))
        return string +"\n"*self.height_margin+""

    def render(self, string:str, filled = True):
        if filled:
            return self._fill_box(string)
        else:
            return string

    def render_cols(self, col_list_str:list, filled = True):
        n_cols = len(col_list_str)
        col_width = int(self.width/n_cols)
        col_max_height = max(l.count("\n") for l in col_list_str)

        frame_str = ""
        for line in range(col_max_height):
            line_str = ""
            line_remaining = None
            for col in col_list_str:
                col_str = ""
                lines = col.split("\n")
                if line_remaining is not None:
                    col_str += line_remaining
                elif len(lines) > line:
                    if len(lines[line])- self._non_printable_len(lines[line]) > col_width:
                        line_size = col_width+self._non_printable_len(lines[line][0:col_width])
                        col_str += lines[line][0:line_size]
                        line_remaining = lines[line][line_size:-1]
                    else:
                        col_str += lines[line]
                col_fill_size = (col_width - len(col_str) + self._non_printable_len(col_str))
                line_str += col_str + " " * col_fill_size
            frame_str += line_str + "\n"
        if filled:
            return self._fill_box(frame_str)
        else:
            return frame_str

    def _non_printable_len(self, string:str):
        matches = re.findall("\x1b.[0-9]*m", string)
        size = 0
        for m in matches:
            size += len(m)
        return size
