from pydub import AudioSegment
from pydub.playback import play
import random
import glob
from time import sleep
from threading import Thread

import config

"""main object to control all 
audio check and organisation"""
class AudioComposer:
    def __init__(self):
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

        self.play_queue = []

        # start thread for EEG
        self.running = True
        t = Thread(target=self.play)
        t.start()

    # receives a signal from main to check & start an audio file
    def play(self):
        while self.running:
            # print('-------- updating audio')

            if len(self.play_queue) > 0:
                print(f'play queue ======   {self.play_queue}')
                if self.check_num_of_players():
                    player_key = self.play_queue.pop()
                    player_key_name = self.list_of_keys[player_key]
                    if self.check_dict_of_players(player_key_name):
                        self.audio_player_bang(player_key_name)
            else:
                sleep(0.1)

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
        if player_key == "engagement":
            config._dict_of_playing["engagement"] = True
            self.engagement.play()
        elif player_key == "excitement":
            config._dict_of_playing["excitement"] = True
            self.excitement.play()
        elif player_key == "focus":
            config._dict_of_playing["focus"] = True
            self.focus.play()
        elif player_key == "interest":
            config._dict_of_playing["interest"] = True
            self.interest.play()
        elif player_key == "relaxation":
            config._dict_of_playing["relaxation"] = True
            self.relaxation.play()
        elif player_key == "stress":
            config._dict_of_playing["stress"] = True
            self.stress.play()

    # crash the threads & processes
    def terminate(self):
        self.running = False

"""Audio Player. 
avoid LOC by instantiating individual 
objects for each pm audio player
"""
class audio_player:
    def __init__(self, performance_metric):
        print(f'spawning audio bot for {performance_metric} player')
        self.performance_metric = performance_metric
        self.audio_folder = glob.glob(f'data/audio/{self.performance_metric}/*.wav')
        self.num_audio_files = len(self.audio_folder)
        print(f'number of files in {performance_metric} folder = {self.num_audio_files}')
        seed_rnd = random.randrange(self.num_audio_files)
        random.seed(seed_rnd)
        random.shuffle(self.audio_folder)

    def play(self):
        # choose random file from self.audio folder
        rnd_audio = random.randrange(self.num_audio_files)
        sound_file = self.audio_folder[rnd_audio]
        print(f'sound file = {sound_file} from {self.performance_metric}')
        sound = AudioSegment.from_wav(sound_file)

        # start a thread and play
        audio_play_thread = Thread(target=play(sound))
        audio_play_thread.start()

        # flag pm in dict as ready to go
        config._dict_of_playing[self.performance_metric] = False

if __name__ == "__main__":
    audiotest = AudioComposer()
