import config
import sub_data as eeg
from audio_composer import AudioComposer
from time import time
from config import *
import trio

def conductor():
    # start the composition timer here
    start_time = time()

    # while the composition duration is less that the duration
    while time() < start_time + config.duration_of_composition:
        pass


def main():
    # 1. connect to EEG reader as a thread
    print("connecting to EEG headset")
    eeg.main()

    # 2. start cello notation as a thread
    print("initiating cello score")

    # 3. starting audio composer
    print("starting audio composer")
    audio_comp = AudioComposer()

    # 4. start the composition
    print("Off we go //////////")


if __name__ =='__main__':
    main()
