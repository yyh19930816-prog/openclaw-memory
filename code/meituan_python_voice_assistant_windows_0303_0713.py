# ZYRON Assistant Core Implementation
# Source: github.com/Surajkumar5050/zyron-assistant
# Date: 2023-11-15
# Description: Local Windows desktop assistant with voice and Telegram control

import os
import sys
import time
import speech_recognition as sr
import psutil
import win32gui
import win32con
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class ZyronAssistant:
    def __init__(self):
        """Initialize assistant with wake word and Telegram token"""
        self.wake_word = "hey pikachu"
        self.telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
        self.bot = None
        self.running = True
        
    def listen_microphone(self):
        """Listen for wake word using microphone"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            
        try:
            text = recognizer.recognize_google(audio).lower()
            if self.wake_word in text:
                print("Wake word detected!")
                self.process_command(text.replace(self.wake_word, "").strip())
        except Exception as e:
            print(f"Error recognizing speech: {e}")

    def process_command(self, command):
        """Process voice or text commands"""
        print(f"Processing command: {command}")
        
        # System commands
        if "battery" in command:
            battery = psutil.sensors_battery()
            response = f"Battery: {battery.percent}% ({'plugged in' if battery.power_plugged else 'not charging'})"
            
        elif "memory" in command:
            mem = psutil.virtual_memory()
            response = f"Memory: {mem.used/1024/1024:.1f}MB used ({mem.percent}%)"
            
        elif "close" in command:
            self.close_active_window()
            response = "Closed active window"
            
        else:
            response = f"Sorry, I didn't understand: {command}"
            
        self.speak_response(response)

    def close_active_window(self):
        """Close currently active window"""
        try:
            window = win32gui.GetForegroundWindow()
            win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            print(f"Error closing window: {e}")

    def speak_response(self, text):
        """Text-to-speech response output"""
        print(f"Assistant: {text}")
        # Would use pyttsx3 or other TTS engine here
        # engine.say(text)
        # engine.runAndWait()

    def telegram_setup(self):
        """Initialize Telegram bot handlers"""
        self.bot = Bot(token=self.telegram_token)
        updater = Updater(token=self.telegram_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.telegram_start))
        dispatcher.add_handler(MessageHandler(Filters.text, self.telegram_message))
        
        updater.start_polling()
        print("Telegram bot started")

    def telegram_start(self, update: Update, context):
        """Handle /start command"""
        update.message.reply_text("ZYRON Assistant ready. Send commands directly.")

    def telegram_message(self, update: Update, context):
        """Process incoming Telegram messages"""
        self.process_command(update.message.text)

    def run(self):
        """Main execution loop"""
        try:
            self.telegram_setup()
            while self.running:
                self.listen_microphone()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down ZYRON Assistant...")
            sys.exit(0)

if __name__ == "__main__":
    assistant = ZyronAssistant()
    assistant.run()