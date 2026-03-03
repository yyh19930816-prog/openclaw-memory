#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows 10 Toast Notifications
Source: https://github.com/jithurjacob/Windows-10-Toast-Notifications
Created: 2023-04-01
Description: Displays Windows 10 Toast Notifications using win10toast library
"""

import time
from win10toast import ToastNotifier

def main():
    """
    Demonstrates usage of Windows 10 Toast Notifications
    """
    # Initialize toast notifier
    toaster = ToastNotifier()
    
    # Basic notification with custom icon (requires .ico file)
    try:
        toaster.show_toast(
            title="Hello World!", 
            msg="Python is 10 seconds awesome!",
            icon_path="custom.ico",  # Path to your .ico file
            duration=10  # Duration in seconds
        )
    except Exception as e:
        print(f"Error showing first toast: {e}")
    
    # Threaded notification - continues execution while showing
    try:
        toaster.show_toast(
            title="Example Two", 
            msg="This notification runs in its own thread!",
            icon_path=None,  # Uses default Windows icon
            duration=5,      # Duration in seconds
            threaded=True    # Runs notification in separate thread
        )
    except Exception as e:
        print(f"Error showing threaded toast: {e}")
    
    # Only needed when using threaded notifications
    # Wait for notification to complete if active
    while toaster.notification_active():
        time.sleep(0.1)
    
    # Success notification
    try:
        toaster.show_toast(
            title="Status Update", 
            msg="All notifications completed successfully!",
            duration=3
        )
    except Exception as e:
        print(f"Error showing final toast: {e}")

if __name__ == "__main__":
    # Check if running on Windows
    import platform
    if platform.system() == "Windows":
        main()
    else:
        print("This script only works on Windows operating systems.")