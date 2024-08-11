from typing import Dict
from pynput.mouse import Button


class MouseLayer:
    def __init__(self, keys_held: Dict, keys_pressed: Dict, keys_released: Dict, mouse_manager) -> None:
        self.slow_mouse_speed = 500
        self.default_mouse_speed = 1800
        self.fast_mouse_speed = 4000
        self.slow_scroll_speed = .1
        self.default_scroll_speed = .5
        self.fast_scroll_speed = 1

        self.keys_held = keys_held
        self.keys_pressed = keys_pressed
        self.keys_released = keys_released
        self.mouse_manager = mouse_manager

    def manage(self, is_activated: bool, delta: float) -> bool:
        # Scroll movement
        if self.keys_held.get("Key.alt_l") and is_activated:
            current_scroll_speed = 0

            if self.keys_held.get("Key.f18"):
                current_scroll_speed = self.slow_scroll_speed
            elif self.keys_held.get("Key.shift"):
                current_scroll_speed = self.fast_scroll_speed
            else:
                current_scroll_speed = self.default_scroll_speed

            if self.keys_held.get("Key.f16"):
                self.mouse_manager.scroll(0, +current_scroll_speed)
            if self.keys_held.get("Key.f14"):
                self.mouse_manager.scroll(0, -current_scroll_speed)
            if self.keys_held.get("Key.f15"):
                self.mouse_manager.scroll(-current_scroll_speed, 0)
            if self.keys_held.get("Key.f17"):
                self.mouse_manager.scroll(+current_scroll_speed, 0)
            return True

        # Mouse movement
        elif is_activated:
            current_mouse_speed = 0
            if self.keys_held.get("Key.f18"):
                current_mouse_speed = self.slow_mouse_speed * delta
            elif self.keys_held.get("Key.shift"):
                current_mouse_speed = self.fast_mouse_speed * delta
            else:
                current_mouse_speed = self.default_mouse_speed * delta

            if self.keys_held.get("Key.f15"):
                self.mouse_manager.move(-current_mouse_speed, +0)
            if self.keys_held.get("Key.f17"):
                self.mouse_manager.move(+current_mouse_speed, +0)
            if self.keys_held.get("Key.f14"):
                self.mouse_manager.move(+0, -current_mouse_speed)
            if self.keys_held.get("Key.f16"):
                self.mouse_manager.move(+0, +current_mouse_speed)

            if self.keys_pressed.get("Key.f20"):
                self.mouse_manager.press(Button.left)
            if self.keys_released.get("Key.f20"):
                self.mouse_manager.release(Button.left)

            if self.keys_pressed.get("Key.f19"):
                self.mouse_manager.press(Button.right)
            if self.keys_released.get("Key.f19"):
                self.mouse_manager.release(Button.right)
            return True
        return False
