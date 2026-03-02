#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Source: github.com/boppreh/keyboard
# Date: 2023-11-20
# Description: Showcases core functionality of keyboard library - event hooks, hotkeys, recording

import keyboard
import time

def main():
    """
    Demonstration of keyboard library's core features:
    - Key press/release simulation
    - Writing text
    - Hotkeys with callbacks
    - Event recording and playback
    - Abbreviations
    """
    
    # Simulate pressing shift+s, then space key
    print("Simulating SHIFT+S, SPACE")
    keyboard.press_and_release('shift+s, space')
    time.sleep(1)
    
    # Write text as if typed
    print("Writing sample text")
    keyboard.write('The quick brown fox jumps over the lazy dog.')
    time.sleep(1)
    
    # Define simple hotkey callback
    def hotkey_callback():
        print("Hotkey CTRL+SHIFT+A pressed!")
    
    print("Press CTRL+SHIFT+A to trigger hotkey")
    keyboard.add_hotkey('ctrl+shift+a', hotkey_callback)
    
    # Define hotkey sequence: PAGE UP then PAGE DOWN writes "foobar"
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))
    print("Press PAGE UP then PAGE DOWN to write 'foobar'")
    
    # Record abbreviations - type @@ then space writes long email
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    print("Type '@@' then SPACE to expand to email")
    
    # Record keyboard events until ESC is pressed
    print("Recording keys (press ESC to stop)...")
    recorded = keyboard.record(until='esc')
    
    # Replay recorded events at 2x speed
    print("Replaying recorded keys...")
    keyboard.play(recorded, speed_factor=2)
    
    # Wait indefinitely until ESC pressed again
    print("Press ESC to exit")
    keyboard.wait('esc')

if __name__ == '__main__':
    main()