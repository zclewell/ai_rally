import pygame
import json
import time

pygame.init()

PLAYBACK_FPS = 30

# Window dimensions
width = 350
height = 300
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
green = (0, 255, 0)
red = (255, 0, 0)

# Input variables (initialize to default values)
steering = 0.0
brake = 0.0
throttle = 0.0
handbrake = 0
clutch = 0

margin = 50

# Slider dimensions and positions
steering_slider_width = width - margin*2
steering_slider_height = 20
steering_slider_x = width // 2 - steering_slider_width // 2
steering_slider_y = 50

pedal_slider_width = 50
pedal_slider_height = 100

brake_slider_x = 50
brake_slider_y = steering_slider_y + steering_slider_height + margin
throttle_slider_x = brake_slider_x + pedal_slider_width + margin
throttle_slider_y = brake_slider_y

# Button dimensions and positions
button_width = 50
button_height = 30
handbrake_button_x = throttle_slider_x + pedal_slider_width + margin
handbrake_button_y = brake_slider_y
clutch_button_x = handbrake_button_x
clutch_button_y = handbrake_button_y + margin

class InputVisualizer():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Driving Game Input Visualizer")
        self.font = pygame.font.Font(None, 36)

    def draw_frame_from_input(self, steering, throttle, brake, handbrake, clutch):

        # Drawing
        self.screen.fill(white)

        # Steering slider
        pygame.draw.rect(self.screen, gray, (steering_slider_x, steering_slider_y, steering_slider_width, steering_slider_height))
        slider_pos = int(steering_slider_x + (steering + 1) / 2 * steering_slider_width)  # Map -1 to 1 to slider position
        pygame.draw.rect(self.screen, black, (slider_pos - 5, steering_slider_y - 5, 10, steering_slider_height + 10))

        # Brake slider
        pygame.draw.rect(self.screen, gray, (brake_slider_x, brake_slider_y, pedal_slider_width, pedal_slider_height))
        slider_pos = int(brake_slider_y + (1 - brake) * pedal_slider_height)  # 0 at bottom, 1 at top
        pygame.draw.rect(self.screen, black, (brake_slider_x - 5, slider_pos - 5, pedal_slider_width + 10, 10))

        # Throttle slider
        pygame.draw.rect(self.screen, gray, (throttle_slider_x, throttle_slider_y, pedal_slider_width, pedal_slider_height))
        slider_pos = int(throttle_slider_y + (1 - throttle) * pedal_slider_height)  # 0 at bottom, 1 at top
        pygame.draw.rect(self.screen, black, (throttle_slider_x - 5, slider_pos - 5, pedal_slider_width + 10, 10))

        # Handbrake button
        color = green if handbrake else red
        pygame.draw.rect(self.screen, color, (handbrake_button_x, handbrake_button_y, button_width, button_height))
        text = self.font.render("HB", True, white)
        self.screen.blit(text, (handbrake_button_x + 5, handbrake_button_y + 5))

        # Clutch button
        color = green if clutch else red
        pygame.draw.rect(self.screen, color, (clutch_button_x, clutch_button_y, button_width, button_height))
        text = self.font.render("CL", True, white)
        self.screen.blit(text, (clutch_button_x + 5, clutch_button_y + 5))

        pygame.display.flip()


if __name__ == '__main__':
    with open('resources/vis_test_inputs.json', 'r') as f:
        inputs = json.loads(f.read())

    vis = InputVisualizer()

    for (_, steering, throttle, brake, handbrake, clutch) in inputs:
        vis.draw_frame_from_input(steering, throttle, brake, handbrake, clutch)

        time.sleep(1.0 / PLAYBACK_FPS)

    pygame.quit()