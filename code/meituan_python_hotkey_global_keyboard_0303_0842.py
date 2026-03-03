#!/usr/bin/env python
# Source: https://github.com/boppreh/keyboard
# Date: 2023-07-20
# Description: Demonstration of keyboard control library with core features

import keyboard
import time

def main():
    """
    Demonstrates keyboard library features including:
    - Key press simulation
    - Writing text
    - Hotkey registration
    - Event recording/playback
    - Abbreviations
    - Event waiting
    """

    # Simulate pressing Shift+S then Space
    print("Simulating Shift+S, Space keys")
    keyboard.press_and_release('shift+s, space')
    time.sleep(1)

    # Write some text automatically
    print("Writing sample text")
    keyboard.write('The quick brown fox jumps over the lazy dog.')
    time.sleep(1)

    # Register simple hotkey Ctrl+Shift+A
    print("Press Ctrl+Shift+A to trigger hotkey")
    keyboard.add_hotkey('ctrl+shift+a', lambda: print("Hotkey triggered!"))
    time.sleep(2)  # Give time to test hotkey

    # Register sequenced hotkey (Page Up then Page Down)
    print("Press Page Up then Page Down to trigger sequenced hotkey")
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))
    time.sleep(2)  # Give time to test sequenced hotkey

    # Add text abbreviation
    print("Type @@ then space to expand abbreviation")
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    time.sleep(2)  # Give time to test abbreviation

    # Record keyboard events until Escape is pressed
    print("\nRecording keystrokes (press ESC to stop)")
    recorded = keyboard.record(until='esc')
    print(f"Recorded {len(recorded)} events")

    # Play back recorded events at double speed
    print("Playing back recorded events")
    keyboard.play(recorded, speed_factor=2)

    # Wait indefinitely for Escape key
    print("\nPress ESC to exit")
    keyboard.wait('esc')

if __name__ == '__main__':
    main()