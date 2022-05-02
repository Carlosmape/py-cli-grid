#!/bin/python
import sys


sys.path.append('../../')

from engine.world.area import area
from engine.engine import Engine
from interface import CommandLineInterface

#########
# Run Engine
# Interface should be changed
#########
interface = CommandLineInterface()
engine = Engine(interface)
engine.run()
