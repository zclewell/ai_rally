import torch
import torch.nn as nn
import torchvision.models as models
from data_collection import XboxController
from input_visualizer import InputVisualizer
import pygame
import time
import mss
import numpy as np
from PIL import Image
import vgamepad as vg

def create_resnet_model(num_classes=5, pretrained=True):
    """Creates a ResNet model with a custom classifier head (two dense layers)."""
    model = models.resnet18()
    in_features = model.fc.in_features

    model.fc = nn.Sequential(
        nn.Linear(in_features, 512),  # First dense layer
        nn.ReLU(),
        nn.Dropout(0.5),  # Dropout after the first layer (optional)
        nn.Linear(512, 256),  # Second dense layer
        nn.ReLU(),
        nn.Dropout(0.5),  # Dropout after the second layer (optional)
        nn.Linear(256, num_classes)  # Output layer
    )

    return model

print('Creating model...')
model = create_resnet_model()

print('Loading weights...')
model.load_state_dict(torch.load('my_model.pth', weights_only=True))

model.eval()  # Set the model to evaluation modes

print('Moving to gpu')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move the model to the GPU if available

region =  {"top": 136, "left": 768, "width": 1024, "height": 1024}

def apply_inputs_to_gamepad(gamepad, inputs):
    steering,  throttle, brake, handbrake, clutch = inputs

    gamepad.right_trigger(value=int(255*throttle))
    gamepad.left_trigger(value=int(255*brake))
    gamepad.left_joystick_float(x_value_float=float(steering), y_value_float=0.0)  # values between -1.0 and 1.0

    gamepad.update()


def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def clamp_outputs(outputs):
    steering, throttle, brake, handbrake, clutch = output[0:]

    steering = clamp(steering, -1.0, 1.0)
    throttle = clamp(throttle, 0.0, 1.0)
    brake = clamp(brake, 0.0, 1.0)
    handbrake = 0.0 if handbrake < 0.5 else 1.0
    clutch = 0.0 if clutch < 0.5 else 1.0

    return steering, throttle, brake, handbrake, clutch
        


with mss.mss() as sct:
    joy = XboxController()
    vis = InputVisualizer()
    gamepad = vg.VX360Gamepad()
    gamepad.reset()

    was_running_inference = False
    should_run_inference = False

    last_ts = time.time()

    target_interval = 1.0 / 15


    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        _, _, _, _, _, start_inference, end_inference = joy.read()

        should_run_inference = start_inference

        if was_running_inference != should_run_inference:
            if should_run_inference:
                print('starting inference')
            else:
                print('ending inference')

            was_running_inference = should_run_inference

        current_ts = time.time()

        if current_ts - last_ts < target_interval:
            continue

        last_ts = current_ts

        if should_run_inference:
            img = sct.grab(region)
            img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            image = np.array(img)[::8,::8,]

            tensor = torch.from_numpy(image).permute(2, 0 , 1).float()
            tensor = tensor.unsqueeze(0)
            tensor = tensor.to(device)

            output = model(tensor)
            output = output[0][0:]

            output = clamp_outputs(output)

            apply_inputs_to_gamepad(gamepad, output)
            vis.draw_frame_from_input(*output)
        else: 
            neutral_output = [0.0, 0.0, 0.0, 0.0, 0.0]
            gamepad.reset()
            apply_inputs_to_gamepad(gamepad,neutral_output)
            vis.draw_frame_from_input(*neutral_output)


            


# print('Exiting')
