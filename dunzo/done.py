import os
from datetime import datetime

from playsound import playsound

# list of available sounds in the library
LIST_OF_SOUNDS = ["flute", "dog", "game"]

DEFAULT_SOUND_DIR = "/sound_effects/"
DEFAULT_SOUND = "flute.wav"
absolute_path = os.path.dirname(os.path.realpath(__file__))


def done(sound="flute") -> str:
    """
    Plays a sound given a sound path.
    """
    if sound in LIST_OF_SOUNDS:
        playsound(f"{absolute_path}{DEFAULT_SOUND_DIR}{sound}.wav")
    else:
        try:
            playsound(sound)
        except:
            print("Problem with your sound file path. Try something else.")

    now = datetime.now().astimezone().strftime("(Date) %Y-%m-%d (Time) %I:%M:%S %p %Z")
    return f"Finished @ {now}"


# TODO:
def slack_done(msg="Hello, your program finished running!"):
    hook_url = ""  # TODO
    os.system(
        "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' %s"
        % (msg, hookurl)
    )
    print("sent slack notification")
