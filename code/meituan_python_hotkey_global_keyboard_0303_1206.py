"""
keyboard Demo Script
Source: https://github.com/boppreh/keyboard
Created: 2023-04-01
Description: Demonstrates core functionality of the keyboard library including
             hotkeys, recording, playback, abbreviations and blocking waits.
"""

import keyboard
import time

def main():
    # Register a simple hotkey that prints when triggered
    print("Registering hotkey: ctrl+alt+h")
    keyboard.add_hotkey('ctrl+alt+h', lambda: print("Hotkey triggered!"))

    # Demonstrate pressing keys programmatically
    print("Simulating key presses: 'Hello World'")
    keyboard.write("Hello World")

    # Record keyboard events until ESC is pressed
    print("\nRecording keyboard events (press ESC to stop)...")
    recorded_events = keyboard.record(until='esc')
    print(f"Recorded {len(recorded_events)} events")

    # Playback recorded events at double speed
    print("Playing back recorded events at 2x speed")
    keyboard.play(recorded_events, speed_factor=2)

    # Setup an abbreviation that expands when typed
    print("\nSetting up abbreviation '@@' -> 'user@example.com'")
    keyboard.add_abbreviation('@@', 'user@example.com')

    # Demonstrate complex hotkey combination
    print("Registering sequence hotkey: ctrl+k then ctrl+b")
    keyboard.add_hotkey('ctrl+k, ctrl+b', lambda: print("Sequence triggered"))

    # Show continuous event monitoring
    print("\nMonitoring keyboard events (press ESC to exit)...")
    keyboard.hook(print)  # Print all keyboard events
    
    # Block until ESC is pressed, with custom message
    print("Blocking until ESC is pressed...")
    keyboard.wait('esc')
    print("ESC pressed, exiting")

    # Cleanup all hotkeys before exiting
    keyboard.unhook_all()
    print("All hooks removed")

if __name__ == "__main__":
    main()