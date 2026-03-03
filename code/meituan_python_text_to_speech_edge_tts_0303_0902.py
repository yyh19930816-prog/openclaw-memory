#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge TTS Python Implementation
Source: GitHub rany2/edge-tts
Date: April 2023
Description: Python module for Microsoft Edge's text-to-speech service
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Optional

# Requires edge-tts package: pip install edge-tts
import edge_tts

async def list_voices(output_format: str = "table") -> None:
    """List all available TTS voices"""
    voices = await edge_tts.VoicesManager.create()
    if output_format == "json":
        print(json.dumps(voices.list, indent=2))
    else:
        print(voices)

async def generate_speech(
    text: str,
    voice: str = "en-US-AriaNeural",
    output_file: Optional[str] = None,
    subtitles_file: Optional[str] = None,
) -> None:
    """
    Generate speech from text using Edge TTS
    
    Args:
        text: Input text to convert to speech
        voice: Voice model to use (e.g., 'en-US-AriaNeural')
        output_file: Path to save audio file (MP3)
        subtitles_file: Path to save subtitles (SRT)
    """
    communicate = edge_tts.Communicate(text, voice)
    
    if output_file:
        # Save audio and optionally subtitles
        sub_maker = edge_tts.SubMaker()
        with open(output_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
        
        if subtitles_file:
            with open(subtitles_file, "w", encoding="utf-8") as file:
                file.write(sub_maker.generate_subs())
        
        print(f"Audio saved to {output_file}")
        if subtitles_file:
            print(f"Subtitles saved to {subtitles_file}")
    else:
        # Stream audio directly if no output file
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                sys.stdout.buffer.write(chunk["data"])

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Edge TTS Python Interface")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--voice", default="en-US-AriaNeural", help="Voice to use")
    parser.add_argument("--write-media", dest="output_file", help="Output audio file (MP3)")
    parser.add_argument("--write-subtitles", dest="subtitles_file", help="Output subtitles file (SRT)")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--json", action="store_true", help="Output voices list as JSON")
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.list_voices:
        asyncio.run(list_voices("json" if args.json else "table"))
    elif args.text:
        asyncio.run(generate_speech(
            args.text,
            args.voice,
            args.output_file,
            args.subtitles_file
        ))
    else:
        print("Error: Either --text or --list-voices must be specified")
        sys.exit(1)

if __name__ == "__main__":
    main()