#!/usr/bin/env python3

"""
Created by: Julianne Leblanc-Peltier
Created on: January 14
This program runs Tetris on the PyBadge using CircuitPython
"""

import stage
import ugame
import time
import random
import constants
from game import Game

def play_tetris() -> None:
    """
    This function plays tetris
    """

    # This bool variable checks if a button is active.
    #   Makes sure that the movement buttons aren't overly sensitive! (must CLICK each time to move)
    active_button = False

    # This counter collects the iteration of the loop.
    #   Makes sure that once a second (60 ticks) the tetris block moves down by 1 block!
    game_loop_counter = 0

    all_blocks = []

    # image banks for Circuit Python
    background_bank = stage.Bank.from_bmp16("/assets/tetris_background.bmp")
    sprite_bank = stage.Bank.from_bmp16("/assets/tetris_sprites.bmp")

    # set the background image to image on pybadge
    #    and the size (10x8 tiles of size 16x16)
    background = stage.Grid(background_bank, 10, 8)


    # create a stage for the background to show up on
    #    and the size (10x8 tiles of size 16x16)
    game = stage.Stage(ugame.display, constants.FPS)

    # set the layers of all sprites, items show up in order
    game.layers = [sprite] + [background]

    # render all sprites
    #    most likely you will only render the background one per game scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # update game logic
        if keys & ugame.K_X:
            print("A")
        elif keys & ugame.K_O:
            print("B")
        elif keys & ugame.K_START:
            print("Start")
        elif keys & ugame.K_SELECT:
            print("Select")
        elif keys & ugame.K_RIGHT:
            if active_button == False:
                # rotates the block 90 degrees clockwise
                game.move_right()
                active_button = True
        elif keys & ugame.K_LEFT:
            if active_button == False:
                game.move_left()
                active_button = True
        elif keys & ugame.K_UP:
            if active_button == False:
                game.rotate()
                active_button = True
        elif keys & ugame.K_DOWN:
            if active_button == False:
                game.move_down()
                active_button = True
        else:
            active_button = False

        # every 60 ticks (1 second), the sprite moves down one block (16 bits).
        if game_loop_counter % 60 == 0:
            game.move_down()

        # checks if sprite is outside of grid limits, readjusts to prior location.
        game.correct_location()      

        # counts the iteration of the loop
        game_loop_counter += 1

        # redraw Sprite
        game.render_sprites([active_tetris_block])
        game.tick()  # wait until refresh rate finishes

if __name__ == "__main__":
    play_tetris()
