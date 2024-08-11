#!/usr/bin/env python

from pynput.keyboard import Controller as keyboard_controller
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller
import time
from layers.mouse_layer import MouseLayer


suppress_key = False

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

    keys_held = {}
    keys_pressed = {}
    keys_released = {}

    mouse_activation_key = "Key.f13"  

    def _parse_key(self, key_event):
        key = str(key_event).replace("'", "")
        return key

    def _on_press(self, key_event):
        key = self._parse_key(key_event)
        self.keys_held[key] = True
        self.keys_pressed[key] = True

    def _on_release(self, key_event):
        key = self._parse_key(key_event)
        self.keys_held[key] = False
        self.keys_released[key] = True

    def _start_key_listener(self):
        self._create_listener()

    def darwin_intercept(event_type, event):
        global suppress_key
        if suppress_key:
            return False
        return event

    def _create_listener(self):
        listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            darwin_intercept=True
        )

        if self.current_listener:
            self.current_listener.stop()

        self.current_listener = listener
        listener.start()

    def start_event_handling(self):
        global suppress_key
        delta_timer = DeltaTimer()
        delta_timer.start()

        mouse_layer = MouseLayer(
            self.keys_held, self.keys_pressed, self.keys_released, self.mouse_manager)

        while True:
            delta = delta_timer.delta()

            is_mouse_activated = self.keys_held.get(
                self.mouse_activation_key, False
            )

            suppress_key = mouse_layer.manage(is_mouse_activated, delta)

            self.keys_pressed.clear()
            self.keys_released.clear()

            time.sleep(0.00833333333)

    def start(self):
        self._start_key_listener()
        self.start_event_handling()


if __name__ == "__main__":
    km = KeyMouse()
    km.start()
