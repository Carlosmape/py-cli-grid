
from engine.menu import Menu
from samples.cli_enhanced.command_line_box import CommandLineBox
from samples.cli_enhanced.render.colors import style


class MenuBox(CommandLineBox):
    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height
    
    def _fill_box(self, string):
        self.height_margin = int(self.height - string.count("\n"))
        return string +"\n"*self.height_margin

    def _render_menu(self, menu: Menu):
        composed_menu = str()

        str_opt=''
        if menu.options:
            i = 0
            for opt in menu.options:
                str_opt += style.CGREEN + str(i)+ "." + style.CEND + str(opt) +" "
                i += 1        

        # Calculate elements size to center the menu
        size_menu = len(menu.title)
        size_query = len(menu.query)
        size_options = len(str_opt)
        max_size_part = max(size_menu, size_options, size_query)

        composed_menu += " "+style.CBOLD+style.CITALIC+menu.title+style.CEND + "\n"
        composed_menu += " "+str_opt + "\n" if str_opt else str_opt
        composed_menu += " "+menu.query.replace("\n", "\n ") 
        return composed_menu

    def render(self, menu: Menu):
        if menu is None:
            return ""
        str_frame  = self._render_menu(menu)
        return self._fill_box(str_frame)

