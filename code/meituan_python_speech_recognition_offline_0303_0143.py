#!/usr/bin/env python3
# Source: https://github.com/alphacep/vosk-api
# Date: 2023-11-20
# Description: Offline speech recognition using Vosk API

import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel

def initialize_model(model_path=None, lang="en"):
    """
    Initialize Vosk speech recognition model.
    If model_path not specified, attempts to find in standard locations.
    
    Args:
        model_path (str): Path to Vosk model directory
        lang (str): Language code (en, fr, de, etc.)
    
    Returns:
        Model: Loaded Vosk model
    """
    if model_path is None:
        # Check standard model locations
        model_path = os.path.join("models", f"vosk-model-small-{lang}-0.22")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Please download from https://alphacephei.com/vosk/models")
    
    print(f"Loading model from {model_path}")
    SetLogLevel(-1)  # Disable most logging
    return Model(model_path)

def transcribe_audio_file(model, audio_path):
    """
    Transcribe audio file using Vosk recognizer.
    
    Args:
        model: Loaded Vosk model
        audio_path: Path to WAV audio file
    
    Returns:
        str: Transcription text
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Open audio file
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
        raise ValueError("Audio file must be WAV format mono PCM")
    
    # Initialize recognizer
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)  # Enable word timestamps
    
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            results.append(result.get("text", ""))
    
    # Get final result
    final_result = json.loads(rec.FinalResult())
    results.append(final_result.get("text", ""))
    
    return " ".join(results).strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python vosk_demo.py <audio_file.wav> [model_path]")
        return
    
    audio_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Initialize model (English by default)
        model = initialize_model(model_path)
        
        # Transcribe audio file
        transcription = transcribe_audio_file(model, audio_path)
        
        print("\nTranscription:")
        print(transcription)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()