import os
from datetime import datetime

from IPython.display import Audio, display

DEFAULT_SOUND_PATH = '/sound_effects/mixkit-retro-game-notification-212.wav'
dir_path = os.path.dirname(os.path.realpath(__file__))

filepath = dir_path + DEFAULT_SOUND_PATH


def done(sound_path=filepath):
    # play sound in ipython
    display(Audio(filename=sound_path, autoplay=True))
    now = datetime.now()
    message = "Finished @ " + now.strftime("%Y-%m-%d, %H:%M:%S")
    return message


def slack_done(msg='Hello, your program finished running!'):
    hook_url = '' # TODO 
    os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' %s" % (msg,hookurl))
    print('sent slack notification')
