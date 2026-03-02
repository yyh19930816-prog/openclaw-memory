#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows 10 Toast Notifications Implementation

Source: github.com/jithurjacob/Windows-10-Toast-Notifications
Date: 2023-03-15
Description: Python script demonstrating Windows 10 toast notifications
using the win10toast library with threading support.
"""

import time
from win10toast import ToastNotifier

def main():
    """
    Main function demonstrating different toast notification examples
    """
    # Initialize the toast notifier
    toaster = ToastNotifier()

    # Example 1: Basic notification (blocks execution for the duration)
    print("Showing basic notification...")
    toaster.show_toast(
        title="Hello World!",
        msg="Python is 10 seconds awesome!",
        icon_path=None,  # Can specify path to custom icon
        duration=10,  # Duration in seconds
        threaded=False  # Blocking (wait for notification to complete)
    )
    print("Basic notification finished!")

    # Example 2: Threaded notification (non-blocking)
    print("\nShowing threaded notification...")
    toaster.show_toast(
        title="Example Two",
        msg="This notification runs in its own thread!",
        icon_path=None,
        duration=5,
        threaded=True  # Non-blocking (runs in background)
    )

    # Example 3: Checking notification status while threaded
    print("\nDemonstrating threaded notification check:")
    print("Notification active:", toaster.notification_active())

    # Wait for threaded notification to complete
    print("Waiting for threaded notification to finish...")
    while toaster.notification_active():
        time.sleep(0.1)
    
    print("All notifications complete!")

    # Example 4: Notification with custom icon
    try:
        print("\nShowing notification with custom icon...")
        toaster.show_toast(
            title="Custom Icon",
            msg="This should show with a custom icon",
            icon_path="custom.ico",  # Replace with actual icon path
            duration=3
        )
    except Exception as e:
        print(f"Could not show notification with custom icon: {e}")

if __name__ == "__main__":
    # Show some console output so we know the program is running
    print("Windows Toast Notification Demo")
    print("------------------------------")
    main()
    print("\nDemo complete!")