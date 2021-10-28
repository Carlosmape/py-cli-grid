from engine.app import *
from interfaces.cli import *

#########
# Run App
# Interface should be changed
#########
interface = CommandLineInterface()
app = App(interface)
app.run()
