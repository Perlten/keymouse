from typing import Dict
from pynput.mouse import Button


class MouseLayer:
    def __init__(self, keys_held: Dict, keys_pressed: Dict, keys_released: Dict, mouse_manager) -> None:
        self.slow_mouse_speed = 300
        self.default_mouse_speed = 2100
        self.fast_mouse_speed = 5400
        self.slow_scroll_speed = 10
        self.default_scroll_speed = 60
        self.fast_scroll_speed = 160
        self.scroll_counter = 0

        self.keys_held = keys_held
        self.keys_pressed = keys_pressed
        self.keys_released = keys_released
        self.mouse_manager = mouse_manager

    def manage(self, is_activated: bool, delta: float):
        # Scroll movement
        if self.keys_held.get("Key.alt") and is_activated:
            current_scroll_speed = 0

            if self.keys_held.get("."):
                current_scroll_speed = self.slow_scroll_speed
            elif self.keys_held.get("-"):
                current_scroll_speed = self.fast_scroll_speed
            else:
                current_scroll_speed = self.default_scroll_speed

            self.scroll_counter += current_scroll_speed * delta

            if self.keys_held.get("w"):
                self.mouse_manager.scroll(0, +self.scroll_counter)
            if self.keys_held.get("s"):
                self.mouse_manager.scroll(0, -self.scroll_counter)
            if self.keys_held.get("a"):
                self.mouse_manager.scroll(-self.scroll_counter, 0)
            if self.keys_held.get("d"):
                self.mouse_manager.scroll(+self.scroll_counter, 0)

            if self.scroll_counter > 1:
                self.scroll_counter = 0
        # Mouse movement
        elif is_activated:
            current_mouse_speed = 0
            if self.keys_held.get("."):
                current_mouse_speed = self.slow_mouse_speed * delta
            elif self.keys_held.get("-"):
                current_mouse_speed = self.fast_mouse_speed * delta
            else:
                current_mouse_speed = self.default_mouse_speed * delta

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
