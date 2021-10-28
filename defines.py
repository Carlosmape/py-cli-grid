#######################
# Defines and constants
#######################

class Position():
    posX = 0
    posY = 0
    posZ = 0
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.posX = x
        self.posY = y
        self.posZ = z
    def __eq__(self, o):
        if type(o) == type(self):        
            return self.posX == o.posX and self.posY == o.posY
        else:
            return False

class ActionType():
    Talk = 0
    Observe = 1
    Stole = 5
    Attack = 6

class ItemAction():
    Observe = 0
    Open = 1
    Take = 2
    Eat = 3
    Equip = 4

class BodyParts():
    head = 0
    shoulder = 1
    arms = 2
    hands = 3
    chest = 4
    core = 5
    legs = 6
    feets = 7

class Sympathy():
    Foe = 0
    Neutral = 1
    Friendly = 2
    Ally = 3

