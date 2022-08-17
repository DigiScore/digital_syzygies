##### user definable composition params #####

# probability of the composition acting on a highest metric (80 % chance of yes)
density = 80

# maximum number of audio files to be played (will only play one from each stream)
max_audio_playing = 4

# minimum duration for cello score onscreen (in seconds)
min_dur_cello_notation = 30

# maximum duraton for cello score onscreen (in seconds)
max_dur_cello_notation = 31

# duration of composition (in seconds)
duration_of_composition = 360

headset = False

full_screen = False

###### non-user variables ####

# the image generated by the random processes in visual.py
image_to_display = " "

# dictonary of audio player status: name of pm: playing status,
_dict_of_playing = {"engagement": False,
                    "excitement": False,
                    "focus": False,
                    "interest": False,
                    "relaxation": False,
                    "stress": False
                    }

_is_playing = False

_current_pm_folder = 'engagement'

_request_access = False

##### Emotiv access and app codes
# client secret = yqqqfzZ297TpeVc05E1Ch9XKkYvZbmgKfqDpGV2SZ5IsCFuR45VdG5K683uNVy2Y4v10oBPFAHC3NnkS3VKsBIrTLcpyykiXT8AIpDQ2coYl2uyyiLD3SutdrHKH703j
# app name = digital_syzygies_no_EEG
# app ID = om.andrewhugill.digital_syzygies_no_eeg
# client Id = B2jzrxVyqPX71AdYLyKn7Ob3SDyTtV15HZRlpxWQ
# EEG = NO
