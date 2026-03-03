# Windows 10 Toast Notifications Demo
# Source: https://github.com/jithurjacob/Windows-10-Toast-Notifications
# Created: 2023-04-01
# Description: Demonstrates toast notifications using win10toast library with threading and custom icons

import time
from win10toast import ToastNotifier

def main():
    """
    Main function demonstrating Windows 10 toast notifications.
    Shows both simple and threaded notifications with custom settings.
    """
    
    # Initialize toast notifier
    toaster = ToastNotifier()
    
    # Example 1: Simple notification with default icon
    print("Displaying simple notification...")
    toaster.show_toast(
        title="Hello World!",
        msg="Python is 10 seconds awesome!",
        icon_path=None,  # None means use default Windows icon
        duration=10,     # Duration in seconds
        threaded=False   # Blocking notification
    )
    
    # Example 2: Threaded notification with custom icon
    print("Displaying threaded notification...")
    try:
        # Try to load custom icon (if available)
        icon_path = "custom.ico"
        toaster.show_toast(
            title="Threaded Notification Example",
            msg="This runs independently in its own thread!",
            icon_path=icon_path,
            duration=5,
            threaded=True  # Non-blocking notification
        )
    except Exception as e:
        # Fallback to default icon if custom icon fails
        print(f"Custom icon not found, using default: {e}")
        toaster.show_toast(
            title="Threaded Notification Example",
            msg="This runs independently in its own thread! (Default Icon)",
            icon_path=None,
            duration=5,
            threaded=True
        )
    
    # Wait for threaded notification to complete if active
    print("Main thread continues while notification displays...")
    while toaster.notification_active():
        time.sleep(0.1)
    
    print("All notifications completed!")

if __name__ == "__main__":
    # Entry point when run as script
    main()