# ZYRON Assistant - Local AI Desktop Companion
# Source: github.com/Surajkumar5050/zyron-assistant
# Date: 2023-11-15
# Description: Voice-controlled local AI assistant with Telegram remote access

import os
import time
import json
import speech_recognition as sr
import psutil
import pyautogui
import requests
from threading import Thread

class ZyronAssistant:
    def __init__(self):
        self.wake_word = "hey pikachu"
        self.running = True
        self.telegram_token = "YOUR_TELEGRAM_TOKEN"
        self.telegram_chat_id = "YOUR_CHAT_ID"
        self.local_ai_url = "http://localhost:11434/api/generate"
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Start Telegram polling thread
        Thread(target=self.telegram_listener).start()

    def listen_for_wake_word(self):
        """Continuously listens for the wake word using microphone"""
        with self.microphone as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            print(f"Listening for wake word '{self.wake_word}'...")

            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if self.wake_word in text:
                        print("Wake word detected! Listening for command...")
                        self.process_command()
                        
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Error in listening: {e}")

    def process_command(self):
        """Processes voice command after wake word detection"""
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=10)
                command = self.recognizer.recognize_google(audio).lower()
                
                print(f"Command received: {command}")
                response = self.query_local_ai(command)
                self.execute_action(command, response)
                
            except Exception as e:
                print(f"Error processing command: {e}")

    def query_local_ai(self, prompt):
        """Queries local Ollama AI for response"""
        try:
            payload = {
                "model": "qwen2.5-coder",
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.local_ai_url, json=payload)
            return response.json().get("response", "I didn't understand that")
        except Exception as e:
            print(f"AI query failed: {e}")
            return None

    def execute_action(self, command, ai_response):
        """Executes appropriate system action based on command"""
        command = command.lower()
        
        # System info commands
        if "battery" in command:
            battery = psutil.sensors_battery()
            status = f"Battery: {battery.percent}% {'Charging' if battery.power_plugged else 'Discharging'}"
            self.speak(status)
            
        elif "memory" in command:
            mem = psutil.virtual_memory()
            status = f"Memory: {mem.percent}% used ({mem.used//1024//1024}MB of {mem.total//1024//1024}MB)"
            self.speak(status)
            
        # Application control
        elif "close" in command and "chrome" in command:
            os.system("taskkill /im chrome.exe /f")
            self.speak("Closed Chrome browser")
            
        elif "open" in command and "notepad" in command:
            os.system("notepad")
            self.speak("Opened Notepad")
            
        else:
            self.speak(ai_response)

    def speak(self, text):
        """Text-to-speech output using Windows built-in voice"""
        os.system(f'PowerShell -Command "Add-Type