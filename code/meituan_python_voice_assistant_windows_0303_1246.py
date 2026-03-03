#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZYRON Desktop Assistant Core Functionality
Source: github.com/Surajkumar5050/zyron-assistant
Date: 2023-11-15
Description: Local AI assistant with voice control and system automation
"""

import os
import subprocess
import speech_recognition as sr
import psutil
import datetime
import platform
from typing import Dict, Any

class ZyronAssistant:
    """Main assistant class handling core functionalities"""
    
    def __init__(self):
        self.wake_word = "hey pikachu"
        self.recognizer = sr.Recognizer()
        self.system_info = self._get_system_info()
        self.commands = {
            "open browser": self._open_browser,
            "system info": self._show_system_info,
            "battery status": self._check_battery,
            "list files": self._list_files,
        }
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect basic system information"""
        return {
            "os": platform.system(),
            "version": platform.version(),
            "processor": platform.processor(),
            "ram": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
            "storage": self._get_storage_info(),
        }
    
    def _get_storage_info(self) -> Dict[str, str]:
        """Get storage information for all drives"""
        partitions = psutil.disk_partitions()
        storage = {}
        for part in partitions:
            usage = psutil.disk_usage(part.mountpoint)
            storage[part.device] = {
                "total": f"{round(usage.total / (1024**3), 2)} GB",
                "used": f"{round(usage.used / (1024**3), 2)} GB",
                "free": f"{round(usage.free / (1024**3), 2)} GB",
                "percent": f"{usage.percent}%"
            }
        return storage
    
    def listen_for_wake_word(self) -> bool:
        """Listen for the wake word using microphone"""
        with sr.Microphone() as source:
            print("Listening for wake word...")
            audio = self.recognizer.listen(source)
            
        try:
            speech = self.recognizer.recognize_google(audio).lower()
            return self.wake_word in speech
        except sr.UnknownValueError:
            return False
    
    def execute_command(self, command: str) -> str:
        """Execute recognized command"""
        for cmd_pattern, func in self.commands.items():
            if cmd_pattern in command.lower():
                return func()
        return "Command not recognized"
    
    def _open_browser(self) -> str:
        """Open default browser"""
        try:
            subprocess.Popen(["start", "https://google.com"], shell=True)
            return "Opening browser..."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _show_system_info(self) -> str:
        """Return formatted system info"""
        info = [f"{k}: {v}" for k, v in self.system_info.items()]
        return "\n".join(info)
    
    def _check_battery(self) -> str:
        """Check battery status"""
        battery = psutil.sensors_battery()
        if battery:
            return (
                f"Battery: {battery.percent}%\n"
                f"Plugged in: {'Yes' if battery.power_plugged else 'No'}\n"
                f"Time left: {str(datetime.timedelta(seconds=battery.secsleft))}"
            )
        return "No battery detected"
    
    def _list_files(self, directory: str = None) -> str:
        """List files in directory"""
        if not directory:
            directory = os.path.expanduser("~")
        try:
            files = os.listdir(directory)
            return "\n".join(files[:10])  # Show first 10 files
        except Exception as e:
            return f"Error: {str(e)}