import os
from py_cli_grid import CommandLineBox

size = os.get_terminal_size()
print("Current terminal size:")
print(f" - Width:{size.columns}")
print(f" - Height: {size.lines}")
screen = CommandLineBox(size.columns, size.lines-6)
sample_box = CommandLineBox(int(size.columns/2), size.lines-6)

print(screen.render_cols([
        sample_box.render("I am\nA text\nOn\nColumn"),\
        sample_box.render("I am\nAnother text\nOn\nAnother Column"),\
    ], False)
)

