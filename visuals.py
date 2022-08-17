import config
import random
from time import sleep
import glob
import threading
from os import path
import sys

# set up local vars
running = True
# path_to_visuals = path.abspath(path.join(path.dirname(__file__),
#                                        '../../data/visuals'))

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    path_to_visuals = path.abspath(path.join(path.dirname(__file__),
                                             '../../data/visuals'))
else:
    # we are running in a normal Python environment
    path_to_visuals = path.abspath(path.join(path.dirname(__file__),
                                             'data/visuals'))

print(f'Path to visuals is {path_to_visuals}')


def update_vis():
    """Thread that chooses a new image per cycle.
    Min and Max durations are defined in the config file.
    File choice is governed by current pm folder in audio selection.
    """

    while running:
        # random dur for image to be on screen
        rnd_dur = random.randrange(config.min_dur_cello_notation,
                                   config.max_dur_cello_notation)

        # current folder params
        current_dir = config._current_pm_folder
        visual_folder_path = path.abspath(path.join(path_to_visuals, current_dir))
        visual_folder = glob.glob(f'{visual_folder_path}/*.jpg')
        image_count = len(visual_folder)
        seed_rnd = random.randrange(image_count)
        random.seed(seed_rnd)
        random.shuffle(visual_folder)
        print(f"{image_count} images in visual folder")
        config.image_to_display = visual_folder[0]

        # random file from visual folder
        rnd_image = random.randrange(image_count)

        # add to the config file
        config.image_to_display = visual_folder[rnd_image]

        # wait out the dur of image on screen
        sleep(rnd_dur)


def terminate():
    """shuts down the thread"""
    global running
    running = False

def main():
    vis_thread = threading.Timer(1, update_vis)
    vis_thread.start()


