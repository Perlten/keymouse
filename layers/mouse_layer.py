from typing import Dict
from pynput.mouse import Button
import time


class MouseLayer:
    def __init__(self, keys_held: Dict, keys_pressed: Dict, keys_released: Dict, mouse_manager) -> None:
        self.slow_mouse_speed = 300
        self.default_mouse_speed = 1800
        self.fast_mouse_speed = 4000
        self.slow_scroll_speed = 1
        self.default_scroll_speed = 2
        self.fast_scroll_speed = 3

        self.keys_held = keys_held
        self.keys_pressed = keys_pressed
        self.keys_released = keys_released
        self.mouse_manager = mouse_manager

    def manage(self, is_activated: bool, delta: float) -> bool:
        # Scroll movement
        if self.keys_held.get("p") and is_activated:
            current_scroll_speed = 0

            if self.keys_held.get("j"):
                current_scroll_speed = self.slow_scroll_speed
            elif self.keys_held.get("key.shift"):
                current_scroll_speed = self.fast_scroll_speed
            else:
                current_scroll_speed = self.default_scroll_speed

            if self.keys_held.get("w"):
                self.mouse_manager.scroll(0, +current_scroll_speed)
            if self.keys_held.get("s"):
                self.mouse_manager.scroll(0, -current_scroll_speed)
            if self.keys_held.get("a"):
                self.mouse_manager.scroll(+current_scroll_speed, 0)
            if self.keys_held.get("d"):
                self.mouse_manager.scroll(-current_scroll_speed, 0)
            return True

        # Mouse movement
        elif is_activated:
            current_mouse_speed = 0
            if self.keys_held.get("j"):
                current_mouse_speed = self.slow_mouse_speed * delta
            elif self.keys_held.get("key.shift"):
                current_mouse_speed = self.fast_mouse_speed * delta
            else:
                current_mouse_speed = self.default_mouse_speed * delta

            if self.keys_held.get("a"):
                self.mouse_manager.move(-current_mouse_speed, +0)
                time.sleep(0.0001)
            if self.keys_held.get("d"):
                self.mouse_manager.move(+current_mouse_speed, +0)
                time.sleep(0.0001)
            if self.keys_held.get("w"):
                self.mouse_manager.move(+0, -current_mouse_speed)
                time.sleep(0.0001)
            if self.keys_held.get("s"):
                self.mouse_manager.move(+0, +current_mouse_speed)
                time.sleep(0.0001)

            if self.keys_pressed.get("key.space"):
                self.mouse_manager.press(Button.left)
            if self.keys_released.get("key.space"):
                self.mouse_manager.release(Button.left)

            if self.keys_pressed.get("k"):
                self.mouse_manager.press(Button.right)
            if self.keys_released.get("k"):
                self.mouse_manager.release(Button.right)
            return True
        return False
