from modules.cortex import Cortex
from audio import AudioComposer
from threading import Thread
import ssl
import websocket  # 'pip install websocket-client' for install
import json
import config
from random import randrange
from time import sleep
from queue import Queue


class Eeg:
    def __init__(self):
        # init values
        self.fields_req_from_met = [1, 3, 6, 8, 10, 12]

        if config.headset:
            url = "wss://localhost:6868"
            sslopt = {"cert_reqs": ssl.CERT_NONE}

            # connect to EEG reader as a thread
            print("connecting to EEG headset")

            # clientId and clientSecret before running script
            your_app_client_id = 'B2jzrxVyqPX71AdYLyKn7Ob3SDyTtV15HZRlpxWQ'
            your_app_client_secret = 'yqqqfzZ297TpeVc05E1Ch9XKkYvZbmgKfqDpGV2SZ5IsCFuR45VdG5K683uNVy2Y4v10oBPFAHC3NnkS3VKsBIrTLcpyykiXT8AIpDQ2coYl2uyyiLD3SutdrHKH703j'

            # s = Subscribe(your_app_client_id, your_app_client_secret)
            self.c = Cortex(your_app_client_id, your_app_client_secret, debug_mode=True)

            print("\n============================")
            print("Connecting to websocket...")
            self.ws = websocket.create_connection(url, sslopt=sslopt)

            # get authorisation
            self.c.authorize(self.ws)
            auth = self.ws.recv()
            print(auth)
            token = json.loads(auth)["result"]["cortexToken"]

            print("Checking headset connectivity...")
            # connect
            self.c.query_headset(self.ws)
            response = self.ws.recv()
            print(response)
            headset_id = json.loads(response)["result"][0]["id"]

            print("Connecting to headset...")

            print("\nCreating session...")
            self.c.create_session(self.ws, token, headset_id)
            response = self.ws.recv()
            print(response)
            session_id = json.loads(response)["result"]["id"]

            print("\nSubscribing to session...")
            stream = ['met']
            self.c.sub_request(stream, self.ws, token, session_id)
            print(self.ws.recv())

        # starting audio composer
        print("starting audio composer")
        self.audio_queue = Queue()
        self.audio = AudioComposer(self.audio_queue)

        t_audio = Thread(target=self.audio.main)
        t_audio.start()

        # start thread for EEG
        self.running = True
        # t = Timer(1, self.read_data)
        t = Thread(target=self.read_data)
        t.start()

    # reads the current metrics and stores in dictionary
    # then does the comparison and calls the audio
    def read_data(self):
        # gets dict from         For example: {'met': [True, 0.5, True, 0.5, 0.0, True, 0.5, True, 0.5, True, 0.5, True, 0.5], 'time': 1627459390.4229}
        while self.running:
            print(f'\t\t\t\taudio players = {config._dict_of_playing}')
            if config.headset:
                print('-------- updating eeg')
                eeg_pm_list = []

                data = json.loads(self.ws.recv())
                data = data['met']
                print('pm data: {}'.format(data))

                # if data != self.eeg_pm_list:
                for field in self.fields_req_from_met:
                    eeg_pm_list.append(data[field])

                # finds position of highest pm_dict into
                highest_pm = self.calc_highest_pm(eeg_pm_list)
                print(f'highest field = {highest_pm}')

                # send the highest pm type position to audio player queue
                # to make sound
                # self.audio.play_queue.append(highest_pm)
                self.audio_queue.put(highest_pm)
            else:
                rnd_pm = randrange(6)
                # self.audio.play_queue.append(rnd_pm)
                self.audio_queue.put(rnd_pm)
                sleep(10)

    def calc_highest_pm(self, pm_dict):
        # calc highest value position of pm
        highest = 0
        highest_value = 0

        for position in range(6):
            if pm_dict[position] > highest_value:
                highest = position
                highest_value = pm_dict[position]

        return highest

    def terminate(self):
        self.running = False
        self.audio.terminate()

if __name__ == "__main__":
    eeg = Eeg()

