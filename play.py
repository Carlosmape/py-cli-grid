from app import *
from interfaces import cli

#########
# Run App
# Interface should be changed
#########
interface = cli.CommandLineInterface()
app = App(interface)
app.run()
