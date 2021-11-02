#!/bin/python

from engine.app import Engine
from interfaces.cli import CommandLineInterface

#########
# Run Engine
# Interface should be changed
#########
interface = CommandLineInterface()
engine = Engine(interface)
engine.run()
