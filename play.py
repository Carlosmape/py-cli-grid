#!/bin/python

from engine.app import App
from interfaces.cli import CommandLineInterface

#########
# Run App
# Interface should be changed
#########
interface = CommandLineInterface()
app = App(interface)
app.run()
