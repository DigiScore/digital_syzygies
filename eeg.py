from modules_new import sub_data
from audio import AudioComposer

class Eeg:
    def __init__(self):
        # connect to EEG reader as a thread
        print("connecting to EEG headset")
        sub_data.main()

        # starting audio composer
        print("starting audio composer")
        engagement_audio = AudioComposer('engagement')

    # reads the current metrics and stores in dictionary
    # then does the comparison and calls the audio
    def read(self):
        # todo - gets dict from         For example: {'met': [True, 0.5, True, 0.5, 0.0, True, 0.5, True, 0.5, True, 0.5, True, 0.5], 'time': 1627459390.4229}
        pm_dict = sub_data.on_new_pow_data()
        # todo parse positin of highest pm_dict into
        highest_pm = self.calc_highest_pm()


    #
    def calc_highest_pm(self):
        # todo calc highest value of pm

        return highest



if __name__ == "__main__":
    eeg = Eeg
