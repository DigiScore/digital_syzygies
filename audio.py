from pydub import AudioSegment
# from pydub.playback import play
from pydub.playback import _play_with_simpleaudio

import random
import glob
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import config

"""main object to control all 
audio check and organisation"""
class AudioComposer:
    def __init__(self):
        # set the running var to go
        self.running = True

        # build an audio player for each of the eeg performance metrics
        engagement = audio_player("engagement")
        excitement = audio_player("excitement")
        focus = audio_player("focus")
        interest = audio_player("interest")
        relaxation = audio_player("relaxation")
        stress = audio_player("stress")

        # set the threads going for the 6 audio players
        tasks = [engagement.play(),
                 excitement.play(),
                 focus.play(),
                 interest.play(),
                 relaxation.play(),
                 stress.play()]

        while self.running:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(task): task for task in tasks}

    # receives a signal from main to check & start an audio file
    def play(self, player_key):
        if self.check_num_of_players():
            if self.check_dict_of_players(player_key):
                self.audio_player_bang(player_key)

    # check to see if pm player is already playing
    def check_dict_of_players(self, player_key):
        if config._dict_of_playing[player_key]:
            return False
        else:
            config._dict_of_playing[player_key] = True
            return True

    # check to see if < max num of players
    def check_num_of_players(self):
        num_of_players = 0
        for key, value in config._dict_of_playing:
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
        elif player_key == "excitement":
            config._dict_of_playing["excitement"] = True
        elif player_key == "focus":
            config._dict_of_playing["focus"] = True
        elif player_key == "interest":
            config._dict_of_playing["interest"] = True
        elif player_key == "relaxation":
            config._dict_of_playing["relaxation"] = True
        elif player_key == "stress":
            config._dict_of_playing["stress"] = True

    # crash the threads & processes
    def terminate(self):
        self.running = False

"""Audio Player. 
avoid LOC by instantiating individual 
objects for each pm audio player
"""
class audio_player:
    def __init__(self, performance_metric):
        self.performance_metric = performance_metric
        self.audio_folder = glob.glob(f'data/audio/{self.performance_metric}/*.wav')
        self.num_audio_files = len(self.audio_folder)
        seed_rnd = random.randrange(self.num_audio_files)
        random.seed(seed_rnd)
        random.shuffle(self.audio_folder)

    def play(self):
        if config._dict_of_playing[self.performance_metric] == True:
            # choose random file from self.audio folder
            rnd_audio = random.randrange(self.num_audio_files)
            sound_file = self.audio_folder[rnd_audio]
            print(f'sound file = {sound_file} from {self.performance_metric}')
            sound = AudioSegment.from_wav(sound_file)
            _play_with_simpleaudio(sound)

            # flag pm in dict as ready to go
            config._dict_of_playing[self.performance_metric] = False

        else:
            sleep(1)


if __name__ == "__main__":
    audiotest = AudioComposer()
