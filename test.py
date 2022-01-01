from pynput.keyboard import Key, Controller as keyboard_controller
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller, Button
import time


some_good_name: set = set()

keyboard_manager = keyboard_controller()
keys_held = {}
keys_pressed = {}
keys_released = {}

def on_press( key_event):
    global some_good_name
    global keys_held
    global keys_pressed
    global keyboard_manager
    
    key = str(key_event).replace("'", "")
    if key in some_good_name:
        some_good_name.remove(key)
        return True

    keys_held[str(key_event).replace("'", "")] = True
    keys_pressed[str(key_event).replace("'", "")] = True
    some_good_name.add(key)

    print("PRESSED: " + key)
    keyboard_manager.press(key)
    
def on_release(key_event):
    global keys_held
    global keys_released
    global keyboard_manager

    key = str(key_event).replace("'", "")
    keys_held[str(key_event).replace("'", "")] = False
    keys_released[str(key_event).replace("'", "")] = True
    
    # keyboard_manager.release(key)

def main():
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True
    )

    listener.start()
    while True:
        time.sleep(0.00833333333)

main()