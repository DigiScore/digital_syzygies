from modules import sub_data
from audio import AudioComposer
import config
from threading import Thread
from modules.sub_data import Subcribe
from concurrent.futures import ThreadPoolExecutor

class Eeg:
    def __init__(self):
        # connect to EEG reader as a thread
        print("connecting to EEG headset")

        # clientId and clientSecret before running script
        your_app_client_id = 'B2jzrxVyqPX71AdYLyKn7Ob3SDyTtV15HZRlpxWQ'
        your_app_client_secret = 'yqqqfzZ297TpeVc05E1Ch9XKkYvZbmgKfqDpGV2SZ5IsCFuR45VdG5K683uNVy2Y4v10oBPFAHC3NnkS3VKsBIrTLcpyykiXT8AIpDQ2coYl2uyyiLD3SutdrHKH703j'

        s = Subcribe(your_app_client_id, your_app_client_secret)

        # list data streams
        streams = ['met']
        #
        # eeg_loop = asyncio.get_event_loop()
        # async_function = asyncio.wait([self.check_video_process_terminate()])
        # eeg_loop.run_until_complete(async_function)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(s.start(streams))}


        # start thread for EEG
        # t = Thread(target=s.start(streams))
        print(' xxxxxxxxxxxxxxxxxx  x   x   x   x   x   x   x   x   got here1')
        # t.start()
        #
        print(' xxxxxxxxxxxxxxxxxx  x   x   x   x   x   x   x   x   got here2')
        # t.join()

        print(' xxxxxxxxxxxxxxxxxx  x   x   x   x   x   x   x   x   got here3')

        # starting audio composer
        print("starting audio composer")
        self.audio_bot = AudioComposer()

    # reads the current metrics and stores in dictionary
    # then does the comparison and calls the audio
    def read_data(self):
        # gets dict from         For example: {'met': [True, 0.5, True, 0.5, 0.0, True, 0.5, True, 0.5, True, 0.5, True, 0.5], 'time': 1627459390.4229}
        pm_dict = config._eeg_data

        # finds position of highest pm_dict into
        highest_pm = self.calc_highest_pm(pm_dict)

        # send the highest pm type position to audio player queue
        # to make sound
        self.audio_bot.play_queue.append((highest_pm))

    def calc_highest_pm(self, pm_dict):
        # calc highest value position of pm
        highest = 0
        highest_value = 0

        for position in range(6):
            if pm_dict[position] > highest_value:
                highest = position
                highest_value = pm_dict[position]

        return highest



if __name__ == "__main__":
    eeg = Eeg
