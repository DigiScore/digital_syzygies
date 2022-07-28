from pydub import AudioSegment
from pydub.playback import play
import random

class AudioComposer:
    def __init__(self):
        # define class params 4 audio composer
        self.list_all_audio = glob.glob('data/audio/*.wav')
        self.num = len(self.list_all_audio)
        seed_rnd = random.randrange(self.num)
        random.seed(seed_rnd)
        random.shuffle(self.list_all_audio)

    def random_design(self):
        # choose a random file
        rnd_file = random.randrange(self.num)
        sound_file = self.list_all_audio[rnd_file]
        print('sound file = ', sound_file)
        sound = AudioSegment.from_wav(sound_file)

        # gain structure for end fade
        if self.aiDirector.globalForm >= 6:
            # reduce the gain by 0.0083 every second for 120 secs
            self.gain -= 0.55

        # play (sound)
        new_sound = self.speed_change(sound, self.gain)
        # length = new_sound.duration_seconds
        # print('length = ', length)
        # fade_sound = new_sound.fade_in(5).fade_out(5)
        return new_sound