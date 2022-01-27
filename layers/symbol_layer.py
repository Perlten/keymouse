from typing import Dict
from utils.config import get_config

class SymbolLayer:

    def __init__(self, keys_held: Dict, keys_pressed: Dict,
                 keys_released: Dict, keyboard_manager
                 ) -> None:
        self.keys_held = keys_held
        self.keys_pressed = keys_pressed
        self.keys_released = keys_released
        self.keyboard_manager = keyboard_manager

    def manage(self, is_activated: bool):
        if is_activated:
            config = get_config()
            mapping: Dict = config["symbol"]["mapping"]

            for key, value in mapping.items():
                if self.keys_pressed.get(key, False):
                    self.keyboard_manager.press(value)

                if self.keys_released.get(key, False):
                    self.keyboard_manager.release(value)
