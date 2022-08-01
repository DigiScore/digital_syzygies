import config
import random
from time import sleep
import glob

import threading

# set up local vars
running = True
visual_folder = glob.glob('data/visuals/*.jpg')
image_count = len(visual_folder)
seed_rnd = random.randrange(image_count)
random.seed(seed_rnd)
random.shuffle(visual_folder)

def update_vis():
    while running:
        rnd_dur = random.randrange(config.min_dur_cello_notation,
                                   config.max_dur_cello_notation)

        config.image_to_display =

        sleep(rnd_dur)

def terminate():
    global running
    running = False

vis_thread = threading.Timer(1, update_vis)
vis_thread.start()


