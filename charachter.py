from defines import *
from items import *

#####################
# Classes and objects
#####################

class Charachter():
    def __init__(self, sName=None, iHealth=100.0, iStreng=1, iAgility=1, iLevel=1, oItems=None, oBag=None):
        self.name = sName or "Unknown charachter"
        self.health = iHealth
        self.maxHealth = iHealth
        self.streng = iStreng
        self.agility = iAgility
        self.level = iLevel
        self.items = oItems or dict.fromkeys([BodyParts.head, BodyParts.shoulder, BodyParts.arms, BodyParts.hands, BodyParts.chest, BodyParts.core, BodyParts.legs, BodyParts.feets], None)
        self.availableActions = dict.fromkeys([ActionType], False)
        self.bag = oBag or list()
        self.position = Position()
        #TODO append items to part dictionary

    def __str__(self):
        return "---\nCharachter:%s\nHealth:%s\nStrength:%s \n---" % (self.name, self.health, self.streng)

class NoPlayerCharachter(Charachter):
    def __init__(self, sName=None, iHealth=100.0, iStreng=1, iAgility=1, iLevel=1, oItems=None, oSympathy=Sympathy.Neutral, oFaction=None, oPosition: Position = Position()):
        super().__init__(self, sName, iHealth, iStreng, iAgility, iLevel, oItems)
        self.position = oPosition
        self.sympathy = oSympathy
        self.faction = oFaction

class PlayerCharachter(Charachter):
    def __init__(self, sName=None, iHealth=100.0, iStreng=1, iAgility=1, iLevel=1, oItems=None, oFaction=None, oPosition: Position = Position()):
        super().__init__(sName, iHealth, iStreng, iAgility, iLevel, oItems)
        self.faction = oFaction
        self.position = oPosition
