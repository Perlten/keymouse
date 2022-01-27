#!/usr/bin/env python3

from pynput.keyboard import Controller as keyboard_controller
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller
import time
import os
import json
from layers.mouse_layer import MouseLayer


def read_config():
    config = {
        "keycode": "135"
    }
    try:
        user_dir = os.path.expanduser("~")
        with open(f'{user_dir}/.config/keymouse/config') as f:
            user_config = json.load(f)
            config.update(user_config)
    except:
        pass
    return config


class DeltaTimer:
    def __init__(self):
        self._start = time.time()
        self._end = None
        self._delta = 0

    def start(self) -> None:
        self._start = time.time()

    def delta(self) -> float:
        if not self._end:
            self._end = time.time()
            self._start = self._end
            return 0

        self._end = time.time()
        self._delta = self._end - self._start

        self._start = self._end
        return self._delta


class KeyMouse:
    mouse_manager = mouse_controller()
    keyboard_manager = keyboard_controller()

    current_listener = None
    is_activated = False

    keys_held = {}
    keys_pressed = {}
    keys_released = {}

    activation_key = "<65493>"  # F24

    def __init__(self, config) -> None:
        self.config = config

    def _set_activation_key(self):
        key_command = f"xmodmap -e 'keycode {self.config['keycode']} = F24'"
        os.system(key_command)

    def parse_key(self, key_event):
        key = str(key_event).replace("'", "")
        return key

    def on_press(self, key_event):
        key = self.parse_key(key_event)
        self.keys_held[key] = True
        self.keys_pressed[key] = True
        # print(self.keys_pressed)

    def on_release(self, key_event):
        key = self.parse_key(key_event)
        self.keys_held[key] = False
        self.keys_released[key] = True
        # print(self.keys_pressed)

    def start_key_listener(self):
        self.create_listener()

    def create_listener(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )

        if self.current_listener:
            self.current_listener.stop()

        self.current_listener = listener
        listener.start()

    def start_event_handling(self):
        delta_timer = DeltaTimer()
        delta_timer.start()

        mouse_layer = MouseLayer(
            self.keys_held, self.keys_pressed, self.keys_released, self.mouse_manager)
        while True:
            delta = delta_timer.delta()

            self.is_activated = self.keys_held.get(self.activation_key, False)
            mouse_layer.manage(self.is_activated, delta)

            if self.is_activated:
                if self.keys_pressed.get("j", False):
                    self.keyboard_manager.press("(")
                    self.keyboard_manager.release("(")

            self.keys_pressed = {}
            self.keys_released = {}

            time.sleep(0.00833333333)

    def start(self):
        self.start_key_listener()
        self.start_event_handling()

if __name__ == "__main__":
    config = read_config()
    km = KeyMouse(config)
    km._set_activation_key()
    km.start()
