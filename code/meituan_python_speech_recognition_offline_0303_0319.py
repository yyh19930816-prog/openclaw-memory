#!/usr/bin/env python3
"""
Vosk API Python Example
Source: https://github.com/alphacep/vosk-api
Date: 2023-11-15
Description: Real-time speech recognition using Vosk offline engine.
Requires: vosk (pip install vosk), sounddevice (pip install sounddevice)
"""

import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

# Configuration parameters
MODEL_PATH = "vosk-model-small-en-us-0.15"  # Download from https://alphacephei.com/vosk/models
SAMPLE_RATE = 16000  # Default sample rate for speech recognition
DEVICE = None  # None means default input device
CHANNELS = 1  # Mono audio input
BLOCKSIZE = 8000  # Audio block size in frames
LATENCY = 'low'  # Low latency recording

def print_devices():
    """List available audio input devices"""
    print("Available audio input devices:")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        print(f"{i}: {dev['name']}")

def main():
    # Check if model exists
    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"Please download the model from {MODEL_PATH}")
        print(f"and unpack as {MODEL_PATH} in the current folder.")
        print(f"Available models: https://alphacephei.com/vosk/models")
        sys.exit(1)

    # Initialize recognizer
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)  # Enable word-level timestamps

    # Audio input queue
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        """Callback function for audio input stream"""
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(bytes(indata))

    try:
        # Show available devices if -l flag is passed
        if len(sys.argv) > 1 and sys.argv[1] == "-l":
            print_devices()
            return

        # Start audio stream
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE,
                             device=DEVICE, channels=CHANNELS,
                             dtype='int16', latency=LATENCY,
                             callback=audio_callback):
            print("Listening... Press Ctrl+C to stop")
            
            while True:
                # Process audio chunks from queue
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    # Final result received
                    result = json.loads(recognizer.Result())
                    print("\nFinal Result:", result['text'])
                else:
                    # Partial result
                    partial = json.loads(recognizer.PartialResult())
                    if 'partial' in partial:
                        print("\rPartial:", partial['partial'], end='', flush=True)

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    main()