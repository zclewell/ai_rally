from inputs import get_gamepad
import pyautogui
import math
import threading
import time
import tqdm
import os
import json

TARGET_FPS = 30
SCREENSHOT_PATH = 'screenshots'



class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        # self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        # self.RightJoystickY = 0
        # self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        # self.RightBumper = 0
        # self.A = 0
        # self.X = 0
        # self.Y = 0
        self.B = 0
        # self.LeftThumb = 0
        # self.RightThumb = 0
        # self.Back = 0
        # self.Start = 0
        # self.LeftDPad = 0
        # self.RightDPad = 0
        # self.UpDPad = 0
        # self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        steering = self.LeftJoystickX
        throttle = self.RightTrigger 
        brake = self.LeftTrigger
        handbrake = self.B
        clutch = self.LeftBumper

        return [steering, throttle, brake, handbrake, clutch]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                # if event.code == 'ABS_Y':
                #     self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                if event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                # elif event.code == 'ABS_RY':
                #     self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                # elif event.code == 'ABS_RX':
                #     self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                # elif event.code == 'BTN_TR':
                #     self.RightBumper = event.state
                # elif event.code == 'BTN_SOUTH':
                #     self.A = event.state
                # elif event.code == 'BTN_NORTH':
                #     self.Y = event.state #previously switched with X
                # elif event.code == 'BTN_WEST':
                #     self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                # elif event.code == 'BTN_THUMBL':
                #     self.LeftThumb = event.state
                # elif event.code == 'BTN_THUMBR':
                #     self.RightThumb = event.state
                # elif event.code == 'BTN_SELECT':
                #     self.Back = event.state
                # elif event.code == 'BTN_START':
                #     self.Start = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY1':
                #     self.LeftDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY2':
                #     self.RightDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY3':
                #     self.UpDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY4':
                #     self.DownDPad = event.state

if __name__ == '__main__':
    joy = XboxController()

    frames = []
    inputs = []
    timestamps = []

    last_ts = time.time()
    interval = 1.0 / TARGET_FPS

    try:
        while True:
            current_ts = time.time()
            if current_ts - last_ts < interval:
                continue
            if current_ts - last_ts > 2*interval:
                print('LAGGING')
            else:
                print(current_ts - last_ts)

            last_ts = current_ts

            frames.append(pyautogui.screenshot())
            inputs.append(joy.read())
            timestamps.append(last_ts)

    except KeyboardInterrupt:
        print('dumping frames to screenshots')

    screenshot_path = SCREENSHOT_PATH + '/' + str(timestamps[0])

    os.mkdir(screenshot_path)

    for i in tqdm.tqdm(range(len(frames))):
        frame = frames[i]
        timestamp = timestamps[i]

        frame.save(f'{screenshot_path}/{timestamp}.png')

    print('saving inputs to json')

    input_json = []
    for input, timestamp in zip(inputs, timestamps):
        input_json.append((timestamp, *input))

    with open(f'{screenshot_path}/inputs.json','w') as f:
        f.write(json.dumps(input_json))


