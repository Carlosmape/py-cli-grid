import os
from py_cli_grid import CommandLineBox, Box

size = os.get_terminal_size()

screen = CommandLineBox(size.columns, size.lines)

horizontal_box = Box(size.columns, int(size.lines/2), False)
str_to_render = f"""
Current terminal size:
 - Width:{size.columns}
 - Height: {size.lines}"""
horizontal_box.setContent(str_to_render)
horizontal_text = horizontal_box.getLines()
print("\n".join(horizontal_text))

column_box1 = Box(int(size.columns/2), int(size.lines/2), True)
column_box1.setContent("1"*int(size.columns/2)*int(size.lines/2))
column_box2 = Box(int(size.columns/2), int(size.lines/2), True)
column_box2.setContent("2"*int(size.columns/2)*int(size.lines/2))
columns_text = column_box1.join(column_box2).getLines()
print("\n".join(columns_text))
