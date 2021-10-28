from defines import *

#####################
# Classes and objects
#####################

class Item():
    def __init__(self, sName=None, sDescription=None, oPosition=None, dicAvailableActions=None):
        self.name = sName or "Empty Item"
        self.description = sDescription or "No description"
        self.Position = oPosition
        if dicAvailableActions is None:
            self.avaliableActions = dicAvailableActions or dict.fromkeys([ItemAction], False)
            self.avaliableActions[ItemAction.Take] = True
            self.avaliableActions[ItemAction.Observe] = True
        else:
            self.avaliableActions = dicAvailableActions

    def __str__(self):
        return "Item: %s\n%s\n%s" % (self.name, self.description, self.avaliableActions)

class Food(Item):
    def __init__(self, sName=None, sDescription=None, oPosition=None, iHealthRecovery=10):
        super().__init__(sName, sDescription, oPosition)
        self.avaliableActions[ItemAction.Eat] = True
        self.healthrecovery = iHealthRecovery
        self.duration=10

class Potion(Item):
    def __init__(self, sName=None, sDescription=None, oPosition=None, iHealthRecovery=10, iAgility=0, iStrength=0):
        super().__init__(sName, sDescription, oPosition)
        self.avaliableActions[ItemAction.Eat] = True
        self.healthrecovery = iHealthRecovery
        self.agilityincrement = iAgility
        self.strenghtincrement = iStreng

class Wearable(Item):
    def __init__(self, sName=None, sDescription=None, oPosition=None, dicAvailableActions=None, bodyPart=None, iHealth=0, iStreng=0, iAgaility=0):
        super().__init__(selft, sName, sDescription, oPosition, dicAvailableActions)
        self.avaliableActions[ItemAction.Equip] = True
        self.part = bodyPart
        self.health = iHealth
        self.streng = iStreng
        self.agility = iAgaility


