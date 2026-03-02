#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Source: https://github.com/boppreh/keyboard
Date: 2023-04-20
Description: Python script demonstrating keyboard control functionality including
             hotkeys, typing, event recording/playback, and abbreviations.
"""

import keyboard
import time

def main():
    """Demonstrate keyboard library functionality."""
    
    # Press Shift+S followed by Space programmatically
    print("Pressing Shift+S and Space...")
    keyboard.press_and_release('shift+s, space')
    time.sleep(1)  # Small delay to observe
    
    # Write some text directly as if typed
    print("Typing a sentence...")
    keyboard.write('The quick brown fox jumps over the lazy dog.')
    time.sleep(1)
    
    # Register a simple hotkey Ctrl+Shift+A
    print("Registering Ctrl+Shift+A hotkey...")
    keyboard.add_hotkey('ctrl+shift+a', lambda: print("Hotkey Ctrl+Shift+A pressed!"))
    print("Press Ctrl+Shift+A to trigger. Press Esc to continue.")
    keyboard.wait('esc')
    
    # Register multi-step hotkey (Page Up then Page Down)
    print("Registering Page Up -> Page Down hotkey...")
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))
    print("Press Page Up then Page Down to type 'foobar'. Press Esc to continue.")
    keyboard.wait('esc')
    
    # Record keyboard events until Esc is pressed
    print("Recording keyboard events (press Esc to stop)...")
    recorded_events = keyboard.record(until='esc')
    print(f"Recorded {len(recorded_events)} events.")
    
    # Play back recorded events at double speed
    print("Playing back recorded events at 2x speed...")
    keyboard.play(recorded_events, speed_factor=2)
    
    # Set up text abbreviation (type @@ then space)
    print("Setting up abbreviation '@@' -> email...")
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    print("Type '@@' then press Space to expand. Press Esc to exit.")
    
    # Block forever until Esc
    keyboard.wait('esc')

if __name__ == '__main__':
    main()