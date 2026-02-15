#!/usr/bin/env python3

"""
Created by: Julianne Leblanc-Peltier
Created on: January 14
This program runs Tetris on the PyBadge using CircuitPython
"""

import ugame
import stage
import random
import time

# ---------------------------------
# Constants
# ---------------------------------
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

GRID_SIZE = 16
BOARD_WIDTH = 10
BOARD_HEIGHT = 8   # smaller so it fits nicely on PyBadge

DROP_SPEED = 0.6

# ---------------------------------
# Base Class
# ---------------------------------
class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


# ---------------------------------
# Tetromino Class
# ---------------------------------
class Tetromino(GameObject):

    SHAPES = [
        [(0,0),(1,0),(2,0),(3,0)],         # I
        [(0,0),(1,0),(0,1),(1,1)],         # O
        [(1,0),(0,1),(1,1),(2,1)],         # T
        [(0,0),(0,1),(1,1),(2,1)],         # J
        [(2,0),(0,1),(1,1),(2,1)],         # L
        [(1,0),(2,0),(0,1),(1,1)],         # S
        [(0,0),(1,0),(1,1),(2,1)]          # Z
    ]

    def __init__(self, bank):
        super().__init__(BOARD_WIDTH // 2, 0)

        self.bank = bank
        self.shape = random.choice(self.SHAPES)
        self.color = random.randint(1,7)

        self.blocks = []
        self.create_sprites()

    def create_sprites(self):
        for block in self.shape:
            sprite = stage.Sprite(self.bank, GRID_SIZE, GRID_SIZE)
            sprite.set_frame(self.color)
            self.blocks.append(sprite)

    def update_sprites(self):
        for i, block in enumerate(self.shape):
            x = (self.x + block[0]) * GRID_SIZE
            y = (self.y + block[1]) * GRID_SIZE
            self.blocks[i].move(x, y)

    def rotate(self):
        # Rotate 90° clockwise around origin
        self.shape = [(-y, x) for (x, y) in self.shape]

    def undo_rotate(self):
        # Rotate back if invalid
        self.shape = [(y, -x) for (x, y) in self.shape]


# ---------------------------------
# Tetris Game Class
# ---------------------------------
class TetrisGame:

    def __init__(self):

        self.display = ugame.display
        self.display.auto_refresh = False

        self.bank = stage.Bank.from_bmp16("/sprites.bmp")

        self.stage = stage.Stage(self.display, 60)
        self.stage.layers = []

        self.locked_blocks = []

        self.current_piece = Tetromino(self.bank)
        self.stage.layers += self.current_piece.blocks

        self.last_drop = time.monotonic()

    # ---------------------------------
    # Collision Detection
    # ---------------------------------
    def is_valid(self, piece, dx=0, dy=0):

        for block in piece.shape:
            new_x = piece.x + block[0] + dx
            new_y = piece.y + block[1] + dy

            if new_x < 0 or new_x >= BOARD_WIDTH:
                return False
            if new_y < 0 or new_y >= BOARD_HEIGHT:
                return False

            for locked in self.locked_blocks:
                if (locked.x // GRID_SIZE == new_x and
                    locked.y // GRID_SIZE == new_y):
                    return False

        return True

    # ---------------------------------
    # Lock Piece
    # ---------------------------------
    def lock_piece(self):
        for sprite in self.current_piece.blocks:
            self.locked_blocks.append(sprite)

        self.current_piece = Tetromino(self.bank)
        self.stage.layers += self.current_piece.blocks

    # ---------------------------------
    # Update
    # ---------------------------------
    def update(self):

        buttons = ugame.buttons.get_pressed()

        if buttons & ugame.K_LEFT:
            if self.is_valid(self.current_piece, dx=-1):
                self.current_piece.move(-1,0)

        if buttons & ugame.K_RIGHT:
            if self.is_valid(self.current_piece, dx=1):
                self.current_piece.move(1,0)

        if buttons & ugame.K_DOWN:
            if self.is_valid(self.current_piece, dy=1):
                self.current_piece.move(0,1)

        if buttons & ugame.K_X:
            self.current_piece.rotate()
            if not self.is_valid(self.current_piece):
                self.current_piece.undo_rotate()

        # Auto drop
        if time.monotonic() - self.last_drop > DROP_SPEED:
            if self.is_valid(self.current_piece, dy=1):
                self.current_piece.move(0,1)
            else:
                self.lock_piece()
            self.last_drop = time.monotonic()

        self.current_piece.update_sprites()

    # ---------------------------------
    # Main Loop
    # ---------------------------------
    def run(self):
        while True:
            self.update()
            self.stage.render_sprites(self.stage.layers)
            self.stage.tick()


# ---------------------------------
# Start Game
# ---------------------------------
if __name__ == "__main__":
    game = TetrisGame()
    game.run()
