from input_visualizer import InputVisualizer
from data_collection import XboxController
import pygame
import time

TARGET_FPS = 30

if __name__ == '__main__':
    joy = XboxController()
    vis = InputVisualizer()

    last_frame_ts = time.time()

    run = True

    while run:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        current_ts = time.time()

        if current_ts - last_frame_ts < 1.0 / TARGET_FPS:
            # too early to draw
            continue

        inputs = joy.read()
        vis.draw_frame_from_input(*joy.read()[:-2])
