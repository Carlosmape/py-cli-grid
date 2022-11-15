#!/bin/python

import sys
sys.path.append('../')

from engine.EngineClient import EngineClient
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.frame import Frame

def print_frame(frame: Frame):
    print("Received a frame!", frame)

if __name__ == "__main__":
    client = EngineClient()
    client.pj = PlayerCharacter("TEST")
    client.on_frame = print_frame
    client.connect()
    client.run()
