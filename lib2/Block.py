#!/usr/bin/env python3

"""
Created by: Julianne Leblanc-Peltier
Created on: February 4
This is a parent/superclass for all universal tetris block attributes
"""
import stage
import ugame
import time
import constants
from position import Position

class Block(stage.Sprite):
    def __init__(self, bank, frame, row_offset = 0, column_offset = 0):

        # attributes
        self.cells = {}
        self.cell_size = 8

        # for multiple blocks
        self.row_offset = row_offset
        self.column_offset = column_offset

        self.x_axis = 72 + self.column_offset
        self.y_axis = 0 + self.row_offset

        # for rotated blocks
        self.rotation_state = 0

        super().__init__(bank, frame, self.x_axis, self.y_axis)

    # functions: move directions, disappear, rotate

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns
        self.move(columns * self.cell_size, rows * self.cell_size)
    
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0
    
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    # personal ones

    def correct_location(self):
        if self.x > 144:
            self.move(144, self.y)
        if self.x < 0:
            self.move(0, self.y)
        if self.y > 120:
            self.move(self.x, 120)
        if self.y < 0:
            self.move(self.x, 0)

    # getters
    def get_reach_limit(self):
        reached_limit = False

        if self.y == 120:
            reached_limit = True
        
        return reached_limit        
