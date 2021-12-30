#!/usr/bin/env python3

from pynput.keyboard import Key, Controller as keyboard_controller
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller, Button
import time


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

    activation_key = "Key.menu"

    def __init__(self) -> None:
        pass

    def on_press(self, key_event):
        self.keys_held[str(key_event).replace("'", "")] = True
        self.keys_pressed[str(key_event).replace("'", "")] = True
        # print(self.keys_pressed)

    def on_release(self, key_event):
        self.keys_held[str(key_event).replace("'", "")] = False
        self.keys_released[str(key_event).replace("'", "")] = True
        # print(self.keys_pressed)

    def start_key_listener(self):
        self.create_listener()

    def create_listener(self, suppress=True):
        self.is_activated = suppress

        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )

        if self.current_listener:
            self.current_listener.stop()

        self.current_listener = listener
        listener.start()

    def start_event_handling(self):
        slow_mouse_speed = 300
        default_mouse_speed = 2100
        fast_mouse_speed = 5400

        delta_timer = DeltaTimer()
        delta_timer.start()

        slow_scroll_speed = 10
        default_scroll_speed = 60
        fast_scroll_speed = 160

        scroll_counter = 0
        while True:
            delta = delta_timer.delta()

            if self.keys_held.get("Key.alt") and self.keys_held.get(
                self.activation_key
            ):
                current_scroll_speed = 0

                if self.keys_held.get("."):
                    current_scroll_speed = slow_scroll_speed
                elif self.keys_held.get("-"):
                    current_scroll_speed = fast_scroll_speed
                else:
                    current_scroll_speed = default_scroll_speed

                scroll_counter += current_scroll_speed * delta

                if self.keys_held.get("w"):
                    self.mouse_manager.scroll(0, +scroll_counter)
                if self.keys_held.get("s"):
                    self.mouse_manager.scroll(0, -scroll_counter)
                if self.keys_held.get("a"):
                    self.mouse_manager.scroll(-scroll_counter, 0)
                if self.keys_held.get("d"):
                    self.mouse_manager.scroll(+scroll_counter, 0)

                if scroll_counter > 1:
                    scroll_counter = 0

            elif self.keys_held.get(self.activation_key):
                current_mouse_speed = 0
                if self.keys_held.get("."):
                    current_mouse_speed = slow_mouse_speed * delta
                elif self.keys_held.get("-"):
                    current_mouse_speed = fast_mouse_speed * delta
                else:
                    current_mouse_speed = default_mouse_speed * delta

                if self.keys_held.get("a"):
                    self.mouse_manager.move(-current_mouse_speed, +0)
                if self.keys_held.get("d"):
                    self.mouse_manager.move(+current_mouse_speed, +0)
                if self.keys_held.get("w"):
                    self.mouse_manager.move(+0, -current_mouse_speed)
                if self.keys_held.get("s"):
                    self.mouse_manager.move(+0, +current_mouse_speed)

                if self.keys_pressed.get("Key.space"):
                    self.mouse_manager.press(Button.left)
                if self.keys_released.get("Key.space"):
                    self.mouse_manager.release(Button.left)

                if self.keys_pressed.get(","):
                    self.mouse_manager.press(Button.right)
                if self.keys_released.get(","):
                    self.mouse_manager.release(Button.right)

            self.keys_pressed = {}
            self.keys_released = {}

            time.sleep(0.00833333333)

    def start(self):
        self.start_key_listener()
        self.start_event_handling()


if __name__ == "__main__":
    km = KeyMouse()
    km.start()
