#!/usr/bin/env python3

"""
Created by: Julianne Leblanc-Peltier
Created on: February 11
This class deals with all game mechanics (ie. movement using keys, locking blocks, etc) of the tetris game.
"""

import stage
import ugame
import time
import random
import constants

class Game:
    def __init__(self, bank):
        self.bank = bank
        self.grid = Grid()
        self.blocks = [One_Block(self.bank), Line_Block(self.bank), L_Block(self.bank), Cube_Block(self.bank)]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
    

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [One_Block(self.bank, 0), Line_Block(self.bank, 1), L_Block(self.bank, 2), Cube_Block(self.bank, 3)]
        block = random.choice(self.blocks)
        self.blocks.remove(block)

        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
    
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
