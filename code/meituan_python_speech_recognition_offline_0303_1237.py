#!/usr/bin/env python3
"""
Vosk Speech Recognition Toolkit Python Example
Source: https://github.com/alphacep/vosk-api
Date: 2023-11-15
Description: Real-time speech recognition from microphone using Vosk
"""

import os
import sys
import argparse
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Vosk Speech Recognition")
    parser.add_argument("--model", type=str, default="vosk-model-small-en-us-0.15",
                       help="Path to Vosk model directory")
    parser.add_argument("--device", type=int, default=None,
                       help="Input device ID (check with sounddevice.query_devices())")
    parser.add_argument("--sample-rate", type=int, default=16000,
                       help="Audio sample rate")
    return parser.parse_args()

def list_devices():
    """List available audio devices"""
    print("Available audio devices:")
    print(sd.query_devices())

def initialize_model(model_path, sample_rate):
    """
    Initialize Vosk model and recognizer
    Args:
        model_path: Path to Vosk model directory
        sample_rate: Audio sample rate
    Returns:
        Tuple of (model, recognizer)
    """
    if not os.path.exists(model_path):
        print(f"Model '{model_path}' not found")
        sys.exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)  # Enable word-level timestamps
    return model, recognizer

def audio_callback(indata, frames, time, status):
    """Called for each audio block from sounddevice"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def run_recognition(device_id, sample_rate):
    """Main recognition loop"""
    try:
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=8000,
            device=device_id,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ) as stream:
            print("#" * 50)
            print("Press Ctrl+C to stop recording")
            print("#" * 50)

            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    print(result)
                # else:
                #     partial = recognizer.PartialResult()
                #     print(partial)

    except KeyboardInterrupt:
        print("\nStopping recognition")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    q = queue.Queue()
    args = parse_args()

    if args.device is None:
        list_devices()
        sys.exit(0)

    _, recognizer = initialize_model(args.model, args.sample_rate)
    run_recognition(args.device, args.sample_rate)