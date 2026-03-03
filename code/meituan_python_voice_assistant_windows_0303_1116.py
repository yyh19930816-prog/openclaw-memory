# ZYRON Desktop Assistant
# Source: https://github.com/Surajkumar5050/zyron-assistant
# Date: 2024-03-20
# Description: Local AI desktop assistant with voice control and Telegram integration

import os
import sys
import json
import time
import threading
import speech_recognition as sr
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class ZyronAssistant:
    def __init__(self):
        self.config = self.load_config()
        self.recognizer = sr.Recognizer()
        self.bot = Bot(token=self.config['telegram_token'])
        self.wake_word = "hey pikachu"
        self.running = True

    def load_config(self):
        """Load configuration from JSON file"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path) as f:
            return json.load(f)

    def listen_for_wake_word(self):
        """Continuously listen for the wake word using microphone"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for wake word...")
            
            while self.running:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if self.wake_word in text:
                        print("Wake word detected!")
                        self.process_voice_command()
                        
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Error: {e}")

    def process_voice_command(self):
        """Process voice command after wake word is detected"""
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = self.recognizer.listen(source, phrase_time_limit=5)
            
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")
                self.execute_command(command)
                
            except sr.UnknownValueError:
                print("Could not understand audio")
            except Exception as e:
                print(f"Error: {e}")

    def execute_command(self, command):
        """Execute the given command"""
        # Simple command execution examples
        if "open browser" in command:
            os.system("start chrome")
            self.speak("Opening browser")
        elif "volume up" in command:
            os.system("nircmd.exe changesysvolume 2000")
            self.speak("Volume increased")
        elif "shutdown" in command:
            self.speak("Shutting down")
            os.system("shutdown /s /t 1")
        else:
            self.speak("Command not recognized")

    def speak(self, text):
        """Convert text to speech (simple version)"""
        print(f"Speaking: {text}")
        # Add actual TTS implementation here

    def telegram_start(self, update: Update, context: CallbackContext):
        """Handle /start command from Telegram"""
        update.message.reply_text(
            "ZYRON Assistant is ready! Send commands to control your PC."
        )

    def telegram_message(self, update: Update, context: CallbackContext):
        """Handle incoming Telegram messages"""
        text = update.message.text.lower()
        self.execute_command(text)
        update.message.reply_text(f"Command executed: {text}")

    def start_telegram_bot(self):
        """Start the Telegram bot in a separate thread"""
        updater = Updater(self.config['telegram_token'], use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.telegram_start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.telegram_message))
        updater.start_polling()
        updater.idle()

    def run(self):
        """Main entry point for the assistant"""
        # Start voice recognition in background thread
        voice_thread = threading.Thread(target=self.listen_for_wake_word)
        voice_thread.daemon = True
        voice_thread.start()

        # Start Telegram