#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edge-tts implementation
Source: https://github.com/rany2/edge-tts
Date: 2023-11-15
Description: Python wrapper for Microsoft Edge's text-to-speech service
"""

import argparse
import asyncio
import logging
from typing import Optional

import edge_tts

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def list_voices() -> None:
    """List all available voices."""
    try:
        voices = await edge_tts.list_voices()
        print("Name                               Gender    ContentCategories      VoicePersonalities")
        print("---------------------------------  --------  ---------------------  --------------------------------------")
        for voice in voices:
            print(f"{voice['Name']:<34} {voice['Gender']:<9} {voice['VoiceType']:<22} {voice['StyleList'][0] if voice['StyleList'] else 'N/A'}")
    except Exception as e:
        logger.error(f"Failed to list voices: {e}")

async def generate_speech(
    text: str,
    voice: str = "en-US-GuyNeural",
    output_file: Optional[str] = None,
    subtitle_file: Optional[str] = None
) -> None:
    """
    Generate speech from text using Edge TTS.
    
    Args:
        text: Input text to convert to speech
        voice: Voice model to use
        output_file: Path to save audio file (MP3)
        subtitle_file: Path to save subtitles file (SRT)
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        if output_file:
            # Save to files if output paths provided
            with open(output_file, "wb") as audio_file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_file.write(chunk["data"])
            
            if subtitle_file:
                with open(subtitle_file, "w", encoding="utf-8") as sub_file:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "WordBoundary":
                            sub_file.write(f"{chunk['offset']}\n{chunk['text']}\n\n")
            
            logger.info(f"Successfully generated files: {output_file}, {subtitle_file}")
        else:
            # Play audio directly if no output file
            player = edge_tts.StreamPlayer()
            await player.play_stream(communicate.stream())
            
    except Exception as e:
        logger.error(f"Speech generation failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Microsoft Edge Text-to-Speech")
    parser.add_argument("--text", help="Text to speak", default="Hello, world!")
    parser.add_argument("--voice", help="Voice to use", default="en-US-GuyNeural")
    parser.add_argument("--write-media", help="Output media file (MP3)")
    parser.add_argument("--write-subtitles", help="Output subtitles file (SRT)")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    
    args = parser.parse_args()
    
    if args.list_voices:
        asyncio.run(list_voices())
    else:
        asyncio.run(generate_speech(
            text=args.text,
            voice=args.voice,
            output_file=args.write_media,
            subtitle_file=args.write_subtitles
        ))

if __name__ == "__main__":
    main()