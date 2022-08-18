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

# print out the contents of each pm folder in the visuals dir
print(f'Path to visuals is {path_to_visuals}')
list_of_keys = ["engagement",
                 "excitement",
                 "focus",
                 "interest",
                 "relaxation",
                 "stress"]

for pm in list_of_keys:
    path_to_pm_vis = path.abspath(path.join(path_to_visuals, pm))
    pm_folder_count = glob.glob(f'{path_to_pm_vis}/*')
    print(f'number of images in {path_to_pm_vis} is {len(pm_folder_count)}')
    random.shuffle(pm_folder_count)


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
        # rnd_file = random.randrange(image_count)
        # seed_rnd = random.randrange(image_count)
        # random.seed(seed_rnd)
        # random.shuffle(visual_folder)
        # config.image_to_display = visual_folder[rnd_file]

        # random file from visual folder
        rnd_image = random.randrange(image_count)

        # add to the config file
        config.image_to_display = visual_folder[rnd_image]

        print(f"taking image from {visual_folder}, file: {config.image_to_display}")

        # wait out the dur of image on screen
        sleep(rnd_dur)


def terminate():
    """shuts down the thread"""
    global running
    running = False

def main():
    vis_thread = threading.Timer(1, update_vis)
    vis_thread.start()


