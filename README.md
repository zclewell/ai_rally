# Ai Rally

Ai agent to play "art of rally" videogame.

## Tools

### data_collection.py

Captures frames and inputs from an Xbox Controller at 30 FPS. Frames are capture from the primary display and the following inputs are collected.
* Left Joystick X (steering): -1.0 - 1.0
* Right Trigger (throttle): 0 - 1.0
* Left Trigger (brake): 0 - 1.0
* Left Shoudler (clutch): 0 or 1.0
* B (handbrake): 0 or 1.0

Frames are stored in the 'screenshots' dir in a subdir with the python timestamp of the first frame. Each frame is titled with the python timestamp of when it was captured. 

Input data is stored in a json file in the same directory as the frames from a collection, they are stored in an ordered tuple of the form (timestamp, steering, throttle, brake, clutch, handbrake).

### the_cooler_data_collection.py

Revision on data_collection.py, inputs.json format is the same but images captured are cropped to 1024x1024

Utlizizes multithreading to offload some of the file IO during collection.

Upon running the script awaits throttle input to start collection. pressing "Y" while collecting data will end the collection

### input_visualizer.py

Library for visualizig input data via pygame. Running it directly will playback a trace of test inputs exercising all inputs.

### realtime_visualizer.py

Tool to visualize inputs from Xbox Controller during data collection.
