# from pydub import AudioSegment
# from pydub.playback import play
from playsound import playsound
import random
import glob
from time import sleep
# from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from os import path
import sys

import config


class AudioComposer:
    """main object to control all
    audio check and organisation"""

    def __init__(self, audio_queue):
        # set the running var to go
        self.running = True
        self.list_of_keys = ["engagement",
                 "excitement",
                 "focus",
                 "interest",
                 "relaxation",
                 "stress"]

        # build an audio player for each of the eeg performance metrics
        self.engagement = audio_player("engagement")
        self.excitement = audio_player("excitement")
        self.focus = audio_player("focus")
        self.interest = audio_player("interest")
        self.relaxation = audio_player("relaxation")
        self.stress = audio_player("stress")

        # self.play_queue = []
        self.audio_queue = audio_queue

        # start thread for EEG
        # t = Thread(target=self.play)
        # t.start()

    def main(self):
        tasks_to_thread = [
            self.play,
            self.engagement.play,
            self.excitement.play,
            self.focus.play,
            self.interest.play,
            self.relaxation.play,
            self.stress.play
            ]

        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(task) for task in tasks_to_thread]

    # receives a signal from main to check & start an audio file
    def play(self):
        while self.running:
            print('-------- updating audio')

            # if len(self.play_queue) > 0:
            try:
                player_key = self.audio_queue.get()
                print(f'player key = {player_key}')

            except Empty:
                sleep(1)

            else:
                # print(f'play queue ======   {self.play_queue}')
                if self.check_num_of_players():
                    # player_key = self.play_queue.pop()
                    player_key_name = self.list_of_keys[player_key]
                    if self.check_dict_of_players(player_key_name):
                        self.audio_player_bang(player_key_name)
                        self.audio_queue.task_done()
            # else:
            #     sleep(1)

    # check to see if pm player is already playing
    def check_dict_of_players(self, player_key):
        # print(self.list_of_keys[player_key])
        if config._dict_of_playing[player_key]:
            return False
        else:
            config._dict_of_playing[player_key] = True
            return True

    # check to see if < max num of players
    def check_num_of_players(self):
        num_of_players = 0
        for key, value in config._dict_of_playing.items():
            if value:
                num_of_players += 1
        if num_of_players <= config.max_audio_playing:
            return True
        else:
            return False

    # once all checks are done bang a go for pm player
    def audio_player_bang(self, player_key):
        config._current_pm_folder = player_key
        if player_key == "engagement":
            config._dict_of_playing["engagement"] = True
            # self.engagement.play()
        elif player_key == "excitement":
            config._dict_of_playing["excitement"] = True
            # self.excitement.play()
        elif player_key == "focus":
            config._dict_of_playing["focus"] = True
            # self.focus.play()
        elif player_key == "interest":
            config._dict_of_playing["interest"] = True
            # self.interest.play()
        elif player_key == "relaxation":
            config._dict_of_playing["relaxation"] = True
            # self.relaxation.play()
        elif player_key == "stress":
            config._dict_of_playing["stress"] = True
            # self.stress.play()
        print(f'playing a {player_key} sample')

    # crash the threads & processes
    def terminate(self):
        self.running = False


class audio_player:
    """Audio Player.
    avoid LOC by instantiating individual
    objects for each pm audio player
    """

    def __init__(self, performance_metric):
        self.running = True
        print(f'spawning audio bot for {performance_metric} player')
        self.performance_metric = performance_metric

        # create path for audio folder
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            path_to_audio_dir = path.abspath(path.join(path.dirname(__file__),
                                                       '../../data/audio'))
        else:
            # we are running in a normal Python environment
            path_to_audio_dir = path.abspath(path.join(path.dirname(__file__),
                                                       'data/audio'))


        # path_to_audio_dir = path.abspath(path.join(path.dirname(__file__),
        #                                      '../../data/audio'))
        path_to_audio = path.abspath(path.join(path_to_audio_dir,
                                               performance_metric))
        print(f'path to audio for {performance_metric} is {path_to_audio}')

        self.audio_folder = glob.glob(f'{path_to_audio}/*.wav')
        self.num_audio_files = len(self.audio_folder)
        print(f'number of files in {performance_metric} folder = {self.num_audio_files}')
        seed_rnd = random.randrange(self.num_audio_files)
        random.seed(seed_rnd)
        random.shuffle(self.audio_folder)

    def play(self):
        while self.running:
            if config._dict_of_playing[self.performance_metric] == True:
                config._is_playing = True
                # print(f'{self.performance_metric} == TRUE')
                # choose random file from self.audio folder
                rnd_audio = random.randrange(self.num_audio_files)
                sound_file = self.audio_folder[rnd_audio]
                print(f'sound file = {sound_file} from {self.performance_metric}; '
                      f'\nrandom number was = {rnd_audio} out of {self.num_audio_files}')
                # sound = AudioSegment.from_wav(sound_file)

                # start a thread and play
                # audio_play_thread = Thread(target=playsound(sound_file))
                # audio_play_thread.start()
                playsound(sound_file)

                # flag pm in dict as ready to go
                config._dict_of_playing[self.performance_metric] = False
                config._is_playing = False

                # print(f'{self.performance_metric} == FALSE')
                print(f'audio is playing ==== {config._is_playing}')

            else:
                sleep(0.1)

if __name__ == "__main__":
    audiotest = AudioComposer()
