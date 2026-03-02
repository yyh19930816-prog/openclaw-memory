#!/usr/bin/env python3
# Source: https://github.com/rany2/edge-tts
# Date: 2023-08-20
# Description: Python script utilizing edge-tts to convert text to speech with Microsoft Edge's TTS service

import asyncio
import argparse
from edge_tts import Communicate, VoicesManager

async def list_voices():
    """List all available voices from Microsoft Edge TTS service"""
    voices = await VoicesManager.create()
    print("{:<35} {:<9} {:<23} {}".format(
        "Name", "Gender", "ContentCategories", "VoicePersonalities"
    ))
    print("-" * 35, "-" * 8, "-" * 22, "-" * 35)
    for voice in voices:
        print("{:<35} {:<9} {:<23} {}".format(
            voice["Name"],
            voice["Gender"],
            ", ".join(voice["ContentCategories"]),
            ", ".join(voice["VoicePersonalities"])
        ))

async def text_to_speech(text, voice, output_file=None, subtitles_file=None):
    """
    Convert text to speech and save to file if specified
    
    Args:
        text: Text to convert to speech
        voice: Name of voice to use
        output_file: Path to save audio file (optional)
        subtitles_file: Path to save subtitles file (optional)
    """
    communicate = Communicate(text, voice)
    
    if output_file is None and subtitles_file is None:
        # Play audio directly if no output files specified
        player = asyncio.create_task(communicate.stream())
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                pass  # Audio is being played by the player task
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")
        await player
    else:
        # Save to files if specified
        submaker = None
        if subtitles_file:
            submaker = communicate.submaker
        
        with open(output_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        
        if subtitles_file and submaker:
            with open(subtitles_file, "w", encoding="utf-8") as file:
                file.write(submaker.generate_subs())

def main():
    parser = argparse.ArgumentParser(
        description="Microsoft Edge Text-to-Speech client"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voices and exit"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to speak"
    )
    parser.add_argument(
        "--voice",
        type=str,
        default="en-US-AriaNeural",
        help="Voice to use (default: en-US-AriaNeural)"
    )
    parser.add_argument(
        "--write-media",
        type=str,
        help="Output audio file path"
    )
    parser.add_argument(
        "--write-subtitles",
        type=str,
        help="Output subtitles file path"
    )
    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(list_voices())
    elif args.text:
        asyncio.run(text_to_speech(
            args.text,
            args.voice,
            args.write_media,
            args.write_subtitles
        ))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()