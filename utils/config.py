import os
import json

from pynput.keyboard import  Key

config = {}


def get_config():
    global config
    if config:
        return config 
    config = {
        "mouse": {
            "keycode": 135
        },
        "symbol": {
            "keycode": 108,
            "mapping": {
                "k": "{",
                "l": "}",
                "d": "(",
                "f": ")",
                "s": ":",
                "e": "=",
                "a": "&",
                "o": "|",
                "q": "!",
                "j": '"',
                "c": "[",
                "v": "]",
                "x": "_",
                "n": "@",
                "<": "\\",
                "g": "$",
            }
        }
    }
    try:
        user_dir = os.path.expanduser("~")
        with open(f'{user_dir}/.config/keymouse/config') as f:
            user_config = json.load(f)
            config.update(user_config)
    except:
        pass
    return config

