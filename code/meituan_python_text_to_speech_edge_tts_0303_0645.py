#!/usr/bin/env python3
# Source: https://github.com/rany2/edge-tts
# Date: 2023-08-20
# Description: Python script to use Microsoft Edge's text-to-speech service
# Supports text-to-speech conversion with voice selection and subtitle generation

import asyncio
from edge_tts import Communicate, VoicesManager
from pathlib import Path
import argparse

async def list_voices():
    """List all available voices from Microsoft Edge TTS service"""
    voices = await VoicesManager.create()
    for voice in voices:
        print(f"{voice['Name']:<35} {voice['Gender']:<8} {voice['ShortName']}")
    return voices

async def text_to_speech(text, voice, output_file, subtitle_file=None):
    """
    Convert text to speech using Edge TTS service
    Args:
        text: Input text to convert
        voice: Voice identifier (e.g., 'en-US-GuyNeural')
        output_file: Path to save audio file (.mp3)
        subtitle_file: Optional path to save subtitles (.srt)
    """
    communicate = Communicate(text, voice)
    
    if subtitle_file:
        subtitle_path = Path(subtitle_file)
        # Ensure parent directory exists
        subtitle_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def on_sentence(start_time, end_time, text):
        """Callback for handling subtitle sentences"""
        if subtitle_file:
            with open(subtitle_file, "a", encoding="utf-8") as file:
                file.write(f"{start_time} --> {end_time}\n{text}\n\n")
    
    # Create or truncate subtitle file
    if subtitle_file:
        with open(subtitle_file, "w", encoding="utf-8") as file:
            file.write("")
    
    # Write audio to file
    await communicate.save(output_file, on_sentence=on_sentence)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Microsoft Edge Text-to-Speech")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--voice", default="en-US-GuyNeural",
                       help="Voice to use (default: en-US-GuyNeural)")
    parser.add_argument("--write-media", help="Output audio file path")
    parser.add_argument("--write-subtitles", help="Output subtitle file path")
    parser.add_argument("--list-voices", action="store_true",
                       help="List all available voices")
    return parser.parse_args()

async def main():
    """Main entry point"""
    args = parse_args()
    
    if args.list_voices:
        await list_voices()
        return
    
    if not args.text:
        print("Error: --text argument is required")
        return
    
    if not args.write_media:
        print("Error: --write-media argument is required")
        return
    
    await text_to_speech(
        text=args.text,
        voice=args.voice,
        output_file=args.write_media,
        subtitle_file=args.write_subtitles
    )
    print(f"Audio saved to {args.write_media}")
    if args.write_subtitles:
        print(f"Subtitles saved to {args.write_subtitles}")

if __name__ == "__main__":
    asyncio.run(main())