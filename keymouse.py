#!/usr/bin/env python3

from pynput.keyboard import Key, Controller as keyboard_controller
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller, Button
from multiprocessing.pool import ThreadPool
import time

class KeyMouse:
    mouse_manager = mouse_controller()
    keyboard_manager = keyboard_controller()

    current_listener = None
    is_activated = False

    keys_pressed = {}

    activation_key = "Key.menu"

    def __init__(self) -> None:
        pass

    def on_press(self, key_event):
        self.keys_pressed[str(key_event).replace("'", "")] = True
        # print(self.keys_pressed)

    def on_release(self, key_event):
        self.keys_pressed[str(key_event).replace("'", "")] = False
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
        fast_mouse_speed = 35
        slow_mouse_speed = 5
   
        current_mouse_speed = fast_mouse_speed
        
        while True:
            if self.keys_pressed.get("Key.alt") and self.keys_pressed.get(self.activation_key):
                if self.keys_pressed.get("w"): 
                    self.mouse_manager.scroll(0, +1)
                if self.keys_pressed.get("s"):
                    self.mouse_manager.scroll(0, -1)

            elif self.keys_pressed.get(self.activation_key):
                if self.keys_pressed.get("<65027>"): # Altgr
                    current_mouse_speed = slow_mouse_speed
                else:
                    current_mouse_speed = fast_mouse_speed

                if self.keys_pressed.get("a"):
                    self.mouse_manager.move(-current_mouse_speed, +0)
                if self.keys_pressed.get("d"):
                    self.mouse_manager.move(+current_mouse_speed, +0)
                if self.keys_pressed.get("w"):
                    self.mouse_manager.move(+0, -current_mouse_speed)
                if self.keys_pressed.get("s"):
                    self.mouse_manager.move(+0, +current_mouse_speed)

                if self.keys_pressed.get("Key.space"):
                    self.mouse_manager.press(Button.left)
                    time.sleep(0.1)
                    self.mouse_manager.release(Button.left)
                    

            time.sleep(0.016)

    def start(self):
        self.start_key_listener()
        self.start_event_handling()




if __name__ == "__main__":
    km = KeyMouse()
    km.start()
