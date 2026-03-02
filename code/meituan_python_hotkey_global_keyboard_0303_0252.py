#!/usr/bin/env python
# Source: https://github.com/boppreh/keyboard
# Date: 2023-11-20
# Description: Demo script showcasing keyboard module functionality - hotkeys, recording, writing, abbreviations

import keyboard
import time

def main():
    """
    Main function demonstrating various keyboard module features.
    """
    
    # 1. Basic key presses and writing
    print("Press Shift+S and Space")
    keyboard.press_and_release('shift+s, space')
    
    time.sleep(1)  # Small delay between actions
    
    print("Writing text...")
    keyboard.write('The quick brown fox jumps over the lazy dog.')
    
    # 2. Hotkey registration
    print("\nRegistered two hotkeys:")
    print("- Ctrl+Shift+A will trigger print function")
    print("- Page Up then Page Down will type 'foobar'")
    
    keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))
    
    # 3. Recording and playback
    print("\nPress keys to record them (ESC to stop)...")
    recorded_events = keyboard.record(until='esc')
    
    print("Playing back recorded keys at 3x speed...")
    keyboard.play(recorded_events, speed_factor=3)
    
    # 4. Abbreviation replacement
    print("\nTry typing '@@' then space to replace with email")
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    
    # 5. Keyboard event hook example
    print("\nListening to keyboard events (press left Windows key to stop)...")
    keyboard.on_press(lambda e: print(f"Key pressed: {e.name}"))
    
    # Block until Windows key is pressed
    keyboard.wait('left windows')
    
    # Clean up hooks
    keyboard.unhook_all()

if __name__ == '__main__':
    print("Keyboard module demonstration")
    print("Press Ctrl+C anytime to exit\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        keyboard.unhook_all()