#!/usr/bin/env python3
# Source: https://github.com/rany2/edge-tts
# Date: 2023-11-20
# Description: Python interface for Microsoft Edge's text-to-speech service

import asyncio
from edge_tts import Communicate, VoicesManager
import argparse
import sys
from typing import Optional, Tuple


async def list_voices() -> None:
    """List all available voices from Microsoft Edge TTS service."""
    voices = await VoicesManager.create()
    for voice in voices.voices:
        print(f"{voice['Name']:40} {voice['Gender']:8} {voice['ContentCategories']:20} {voice['VoicePersonalities']}")


async def text_to_speech(
    text: str,
    voice: str = "en-US-GuyNeural",
    output_file: Optional[str] = None,
    subtitle_file: Optional[str] = None,
    playback: bool = False
) -> None:
    """
    Convert text to speech using Microsoft Edge TTS service.
    
    Args:
        text: Input text to convert
        voice: Voice to use (default: en-US-GuyNeural)
        output_file: Optional path to save audio (MP3)
        subtitle_file: Optional path to save subtitles (SRT)
        playback: Whether to play audio immediately
    """
    communicate = Communicate(text, voice)
    
    if output_file:
        # Save audio and optionally subtitles
        await communicate.save(output_file)
        if subtitle_file:
            submaker = communicate.submaker
            with open(subtitle_file, "w", encoding="utf-8") as file:
                file.write(submaker.generate_subs())

    if playback:
        # Play audio with built-in playback
        player = asyncio.create_task(communicate.stream())
        await player


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Microsoft Edge Text-to-Speech")
    subparsers = parser.add_subparsers(dest="command")

    # List voices command
    list_parser = subparsers.add_parser("list", help="List available voices")

    # Convert text command
    convert_parser = subparsers.add_parser("convert", help="Convert text to speech")
    convert_parser.add_argument("--text", required=True, help="Text to convert")
    convert_parser.add_argument("--voice", default="en-US-GuyNeural", help="Voice to use")
    convert_parser.add_argument("--output", help="Output audio file (MP3)")
    convert_parser.add_argument("--subtitles", help="Output subtitle file (SRT)")
    convert_parser.add_argument("--playback", action="store_true", help="Play audio immediately")

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    if args.command == "list":
        await list_voices()
    elif args.command == "convert":
        await text_to_speech(
            args.text,
            args.voice,
            args.output,
            args.subtitles,
            args.playback
        )
    else:
        print("Please specify a command: list or convert")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)