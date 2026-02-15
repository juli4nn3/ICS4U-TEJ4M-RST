#!/usr/bin/env python3

"""
Created by: Julianne Leblanc-Peltier
Created on: February 11
These are all of the subclasses of Block superclass, each being a distinctly shaped tetris block.
"""

import stage
import ugame
import time
import constants
from position import Position
from block import Block

class One_Block(Block):
    def __init__(self, bank, frame = 0):

        super().__init__(bank, frame, identity=1)

        self.cells = {
            0: [Position(self.x_axis, self.y_axis)]
        }

        self.move(0, 9)


class IBlock(Block):
    def __init__(self, bank, frame = 1):

        frame1 = 1
        frame2 = 2
        frame3 = 3

        block1 = super().__init__(bank, frame1, identity=2)
        block2 = super().__init__(bank, frame2, identity=2.1)

        # object attributes
        self.x_axis = 72
        self.y_axis = 0

        self.cells = {
            0: [Position(0, 0), Position(0, 1)],
            1: [Position(0, 0), Position(1, 0)]
        }

        self.move(0, 9)

class LBlock(Block):
    def __init__(self, bank, frame = 5):

        frame1 = 5
        frame2 = 6
        frame3 = 7
        frame4 = 8

        super().__init__(bank, frame, identity=3)

        # object attributes
        self.x_axis = 72
        self.y_axis = 0

        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,0)],
            1: [Position(0,0), Position(0,1), Position(1,1)],
            2: [Position(0,1), Position(1,0), Position(1,1)],
            3: [Position(0,0), Position(1,0), Position(1,1)]
        }

        self.move(0, 9)

class OBlock(Block):
    def __init__(self, bank, frame = 9):

        frame1 = 9
        frame2 = 10
        frame3 = 11
        frame4 = 12

        super().__init__(bank, frame, identity=4)

        # object attributes
        self.x_axis = 72
        self.y_axis = 0

        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)]
        }

        self.move(0, 9)
