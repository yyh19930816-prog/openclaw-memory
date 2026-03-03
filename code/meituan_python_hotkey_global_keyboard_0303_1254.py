#!/usr/bin/env python
# Source: https://github.com/boppreh/keyboard
# Date: 2023-11-20
# Description: Demonstrate core keyboard automation features - hotkeys, recording, typing, etc.

import keyboard
import time

def main():
    """
    Main function demonstrating keyboard automation features.
    """
    # Example 1: Simulate key presses
    print("Example 1: Simulating 'shift+s' then space")
    keyboard.press_and_release('shift+s, space')
    time.sleep(1)  # Small delay between examples

    # Example 2: Typing text
    print("\nExample 2: Typing text")
    keyboard.write('Hello from keyboard module!')
    time.sleep(1)

    # Example 3: Registering hotkeys
    print("\nExample 3: Registering hotkeys - press Ctrl+Shift+A or Page Up then Page Down")
    keyboard.add_hotkey('ctrl+shift+a', lambda: print("Hotkey Ctrl+Shift+A pressed!"))
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('hotkey triggered!'))
    time.sleep(5)  # Give time to test hotkeys

    # Example 4: Recording and replaying events
    print("\nExample 4: Recording keys for 5 seconds (press some keys)")
    recorded = keyboard.record(until='esc')  # Press ESC to stop
    print("Replaying recorded keys...")
    keyboard.play(recorded, speed_factor=2)  # Double speed replay

    # Example 5: Text abbreviation
    print("\nExample 5: Type '@@' followed by space to expand")
    keyboard.add_abbreviation('@@', 'long.email@example.com')

    # Wait indefinitely
    print("\nPress ESC to exit or test other features...")
    keyboard.wait('esc')  # Block until ESC is pressed

if __name__ == "__main__":
    main()