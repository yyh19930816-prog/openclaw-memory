#!/usr/bin/env python3
# Source: https://github.com/rany2/edge-tts
# Date: 2023-11-28
# Description: Python interface to Microsoft Edge's text-to-speech service

import asyncio
import json
from typing import Optional, Dict, List
import os
import argparse
from edge_tts import Communicate, VoicesManager

async def list_voices(filter_lang: Optional[str] = None) -> List[Dict]:
    """List available voices with optional language filter
    
    Args:
        filter_lang: Language code to filter voices (e.g. 'en-US')
    
    Returns:
        List of voice dictionaries with name, gender, etc.
    """
    voices = await VoicesManager.create()
    if filter_lang:
        return voices.find(Language=filter_lang)
    return voices.voices

async def text_to_speech(
    text: str,
    output_file: str,
    voice: str = "en-US-AriaNeural",
    rate: str = "+0%",
    volume: str = "+0%",
    subtitle_file: Optional[str] = None
) -> None:
    """Convert text to speech and save as audio file
    
    Args:
        text: Input text to synthesize
        output_file: Path to save audio (e.g. 'output.mp3')
        voice: Voice name from list_voices()
        rate: Speaking rate adjustment (+/- percentage)
        volume: Volume adjustment (+/- percentage)
        subtitle_file: Optional path to save subtitles (SRT format)
    """
    communicate = Communicate(text, voice, rate=rate, volume=volume)
    
    # Setup output streams
    streams = [communicate.stream()]
    if subtitle_file:
        streams.append(communicate.save_subtitle(subtitle_file))
    
    # Write audio file
    with open(output_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
    
    print(f"Audio saved to {output_file}")
    if subtitle_file:
        print(f"Subtitles saved to {subtitle_file}")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Microsoft Edge TTS')
    parser.add_argument('--text', help='Text to speak', required=True)
    parser.add_argument('--voice', help='Voice name', default="en-US-AriaNeural")
    parser.add_argument('--output', help='Output audio file', default="output.mp3")
    parser.add_argument('--subtitles', help='Output subtitle file')
    parser.add_argument('--rate', help='Speech rate adjustment', default="+0%")
    parser.add_argument('--volume', help='Volume adjustment', default="+0%")
    parser.add_argument('--list-voices', action='store_true', help='List available voices')
    parser.add_argument('--filter-lang', help='Filter voices by language code')
    return parser.parse_args()

async def main():
    args = parse_args()
    
    if args.list_voices:
        # List available voices
        voices = await list_voices(args.filter_lang)
        print(json.dumps(voices, indent=2))
        return
    
    # Convert text to speech
    await text_to_speech(
        text=args.text,
        output_file=args.output,
        voice=args.voice,
        rate=args.rate,
        volume=args.volume,
        subtitle_file=args.subtitles
    )

if __name__ == "__main__":
    asyncio.run(main())