import random

from defines import *
from items import *
from charachter import *

class Room():
    def __init__(self, isInitialRoom=False, template=None):
        if template is None:
            self.generateRandom(isInitialRoom)
        else:
            self.loadTemplate(isInitialRoom, template)

    def generateRandom(self, isInitialRoom):
        self.height = random.randint(10, 20)
        self.width = random.randint(10, 20)
        iNumItems = random.randint(0, int(self.height*self.width/7))
        if  isInitialRoom:
            iNumDoors = random.randint(1, 5)
            iNumFoes = random.randint(0, 5)
        else:
            iNumDoors = random.randint(0, 5)
            iNumFoes = random.randint(1, 6)


    def loadTemplate(self, isInitialRoom, template):
        self.height = 0
        #TODO implement this



