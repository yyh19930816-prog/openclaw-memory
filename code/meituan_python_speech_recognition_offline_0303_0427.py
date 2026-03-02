#!/usr/bin/env python3
"""
Vosk Speech Recognition Toolkit - Python Demo
Source: https://github.com/alphacep/vosk-api
Date: 2023-11-20
Description: Real-time speech recognition from microphone using Vosk
"""

import os
import sys
import argparse
import queue
import threading
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Vosk Speech Recognition Demo")
    parser.add_argument("-m", "--model", type=str, default="vosk-model-small-en-us-0.15",
                       help="Path to the Vosk model directory")
    parser.add_argument("-d", "--device", type=int, default=None,
                       help="Input device ID (check with sounddevice.query_devices())")
    parser.add_argument("-r", "--sample-rate", type=int, default=16000,
                       help="Sampling rate in Hz")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Show verbose output")
    return parser.parse_args()

def audio_callback(indata, frames, time, status, q):
    """Sounddevice callback to put audio data in queue"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def recognize_from_microphone(model_path, device_id, sample_rate):
    """Perform real-time speech recognition from microphone"""

    # Load Vosk model
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Please download it from https://alphacephei.com/vosk/models")
        sys.exit(1)
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)

    # Initialize audio queue and stream
    audio_queue = queue.Queue()
    stream = sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=8000,
        device=device_id,
        dtype="int16",
        channels=1,
        callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, audio_queue)
    )

    print("Listening... Press Ctrl+C to stop")

    try:
        with stream:
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    print(result if args.verbose else result.split('"text"')[1][3:-2])
                else:
                    partial = recognizer.PartialResult()
                    if args.verbose:
                        print(partial)

    except KeyboardInterrupt:
        print("\nRecognition stopped")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    args = parse_args()
    recognize_from_microphone(args.model, args.device, args.sample_rate)