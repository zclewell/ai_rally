import mss
import time
import queue
import threading
import tqdm
import json
import os

from data_collection import XboxController

TARGET_FPS = 10.0

region =  {"top": 136, "left": 768, "width": 1024, "height": 1024}

should_run = True

def try_drain_queue_and_save_file(screenshot_queue):
    if not screenshot_queue.empty():
        ts, ss = screenshot_queue.get()

        mss.tools.to_png(ss.rgb, ss.size, output=f'{prefix}/{ts}.png')

        screenshot_queue.task_done()


def file_writer_worker(screenshot_queue):
    while should_run:
        try_drain_queue_and_save_file(screenshot_queue)

    # Collection stopped, drain any screen shots in queue
    print('draining queue')

    for _ in tqdm.tqdm(range(screenshot_queue.qsize())):
        if (screenshot_queue.empty()):
            break
        try_drain_queue_and_save_file(screenshot_queue)


screenshot_queue = queue.Queue()
file_writer_thread = threading.Thread(target=file_writer_worker, args=(screenshot_queue,))
file_writer_thread.start()

last_ts = time.time()
interval = 1.0/TARGET_FPS

joy = XboxController()

inputs = []

prefix = f'datacollects/{time.time()}'

os.mkdir(prefix)

try:
    with mss.mss() as sct:
        print('waiting for throttle input to start collection')
        while should_run:
            _, throttle, _, _, _, _, _ = joy.read()

            # Avoid using 0 in case of controller drift
            if throttle > 0.01:
                print('starting collection')
                break

        while should_run:
            current_ts = time.time()

            if (current_ts - last_ts) < interval:
                continue
            if (current_ts - last_ts) > 2*interval:
                print(f'{current_ts}: LAG')

            last_ts = current_ts

            steering, throttle, brake, handbrake, clutch, quit, _ = joy.read()

            inputs.append((last_ts, steering, throttle, brake, handbrake, clutch))
            ss = sct.grab(region)

            screenshot_queue.put((last_ts, ss))

            if quit:
                should_run = False
                print('early stopping')
except:
    should_run = False

with open(f'{prefix}/inputs.json', 'w') as f:
    f.write(json.dumps(inputs))

file_writer_thread.join()