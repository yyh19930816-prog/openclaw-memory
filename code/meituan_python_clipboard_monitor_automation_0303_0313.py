#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source: https://github.com/XingYuan55/autoreplier
# Date: 2023-03-15
# Description: AI Auto Replier for WeChat messages with clipboard monitoring

import time
import win32clipboard
import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
import json

class ChatWindow:
    """Handles WeChat window interactions and message capture"""
    
    def __init__(self):
        self.window_title = "WeChat"
        self.settings = self._load_settings()
        
    def _load_settings(self):
        """Load settings from JSON file"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "message_box_pos": None,
                "send_button_pos": None,
                "chat_title_pos": None,
                "ai_params": {}
            }

    def focus_window(self):
        """Bring WeChat window to focus"""
        try:
            win = gw.getWindowsWithTitle(self.window_title)[0]
            win.activate()
            time.sleep(0.5)
            return True
        except IndexError:
            return False

    def capture_message(self):
        """Capture the latest message using clipboard"""
        try:
            self.focus_window()
            
            # Copy message text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            # Get clipboard content
            win32clipboard.OpenClipboard()
            message = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            return message.strip()
        except Exception:
            return None

    def send_reply(self, reply_text):
        """Send reply message"""
        try:
            self.focus_window()
            
            # Type and send reply
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(reply_text)
            win32clipboard.CloseClipboard()
            
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            pyautogui.press('enter')
            return True
        except Exception:
            return False

class ChatSession:
    """Manages the chat session flow with AI integration"""
    
    def __init__(self):
        self.chat_window = ChatWindow()
        self.stop_flag = False
        
    def process_with_ai(self, message):
        """Simulate AI processing - in real implementation use AI API"""
        # This is a placeholder - replace with actual AI call
        return f"AI Reply to: {message[:50]}..."
    
    def monitor(self):
        """Main monitoring loop"""
        print("Starting WeChat message monitor...")
        last_message = ""
        
        try:
            while not self.stop_flag:
                # Check clipboard for new messages
                current_message = self.chat_window.capture_message()
                
                if current_message and current_message != last_message:
                    print(f"New message: {current_message[:50]}...")
                    
                    # Process with AI
                    reply = self.process_with_ai(current_message)
                    print(f"AI Reply: {reply[:50]}...")
                    
                    # Send reply
                    self.chat_window.send_reply(reply)
                    last_message = current_message
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    session = ChatSession()
    session.monitor()