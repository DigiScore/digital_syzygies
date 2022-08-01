from pydub import AudioSegment
from pydub.playback import play
import random
import glob
import trio
import config


class AudioComposer:
    def __init__(self, audio_folder):
        self.running = True

        # define class params 4 audio composer
        self.list_all_audio = glob.glob('data/audio/*.wav')
        self.num = len(self.list_all_audio)
        seed_rnd = random.randrange(self.num)
        random.seed(seed_rnd)
        random.shuffle(self.list_all_audio)

        self.dict_of_playing = {"excitement": False,
                                "2": False,
                                "3": False,
                                "4": False,
                                "5": False,
                                "6": False}

        self.start_players()

    def start_players(self):
        executor = ThreadPoolExecutor(max_workers=4)
        executor.submit(wait_on_future)

    def play(self, player_key):
        if self.check_num_of_players():
            if self.check_dict_of_players(player_key):
                self.audio_player(player_key)

    def check_dict_of_players(self, player_key):
        if self.dict_of_playing[player_key]:
            return False
        else:
            self.dict_of_playing[player_key] = True
            return True

    def check_num_of_players(self):
        num_of_players = 0
        for key, value in self.dict_of_playing:
            if value:
                num_of_players += 1
        if num_of_players <= config.max_audio_playing:
            return True
        else:
            return False

    def terminate(self):
        self.running = False

    def audio_player(self, player_key):
        while self.running:
            if self.dict_of_playing["excitement"]:


    async def child1():
        print("  child1: started! sleeping now...")
        await trio.sleep(1)
        print("  child1: exiting!")

    async def child2():
        print("  child2: started! sleeping now...")
        await trio.sleep(1)
        print("  child2: exiting!")

    async def parent():
        print("parent: started!")
        async with trio.open_nursery() as nursery:
            print("parent: spawning child1...")
            nursery.start_soon(child1)

            print("parent: spawning child2...")
            nursery.start_soon(child2)

            print("parent: waiting for children to finish...")
            # -- we exit the nursery block here --
        print("parent: all done!")

    trio.run(parent)













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