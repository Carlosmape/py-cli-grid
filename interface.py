import time
import os

from defines import *
from items import *
from charachter import *
from room import *
from frame import *

###########
# Base Interface class 
# (should not be instantiated, should be used as base class and use child instances)
###########
class Interface():
    def __init__(self):
        #Defines frame interval in seconds
        self.maxFrameRate = 25
        self.lastUpdate=time.time()

    # Public method to Display a Frame. 
    def displayFrame(self, frame: Frame): 
        self.__tryRender(frame)

    # Public method to Display a Menu (without Frame)
    def displayMenu(self, menu: Menu):
        self.render(menu)
    
    # Public method to get user input (must be overrided)
    def readUserInput(self):
        raise NotImplementedError()

    # Render a frame within maxframerate
    def __tryRender(self, frame: Frame):
        if time.time() - self.lastUpdate > 1/self.maxFrameRate:
            self.lastUpdate = time.time()
            self.render(frame)

    # Render a frame without maxframerate 
    def render(self, frame: Frame):
        raise NotImplementedError()

