import os
from py_cli_grid import CommandLineBox

size = os.get_terminal_size()

screen = CommandLineBox(size.columns, size.lines)
horizontal_box = CommandLineBox(size.columns, int(size.lines/2))

horizontal_text=horizontal_box.render("""Current terminal size:
 - Width:{size.columns}
 - Height: {size.lines}""")

column_text = horizontal_box.render_cols([
    ("1"*int(size.columns/2-1)+"\n")*int(size.lines/2),
    ("2"*int(size.columns/2-1)+"\n")*int(size.lines/2)])

print(horizontal_text + column_text)

