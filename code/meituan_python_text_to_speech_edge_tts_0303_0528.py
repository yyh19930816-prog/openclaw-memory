#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Source: https://github.com/rany2/edge-tts
# Date: 2023-03-15
# Description: Python wrapper for Microsoft Edge's text-to-speech service
# Allows text-to-speech conversion with voice selection and subtitle generation

import argparse
import asyncio
from edge_tts import Communicate, VoicesManager

async def list_voices():
    """List all available voices from Microsoft Edge TTS service"""
    voices = await VoicesManager.create()
    print("Name                               Gender    ContentCategories      VoicePersonalities")
    print("---------------------------------  --------  ---------------------  --------------------------------------")
    for voice in voices.all_voices:
        print(f"{voice['ShortName']:<34} {voice['Gender']:<9} {voice['VoiceType']:<22} {voice.get('StyleList', ['N/A'])[0]}")

async def generate_speech(text, voice, media_file, subtitle_file):
    """
    Generate speech from text using selected voice
    Save audio to media_file and subtitles to subtitle_file
    """
    communicate = Communicate(text, voice)
    submaker = None
    
    if subtitle_file:
        submaker = communicate.subtitle
        submaker.set_subtitle_type("srt")
    
    with open(media_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
    
    if subtitle_file:
        with open(subtitle_file, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())

async def playback(text, voice):
    """Play the generated speech directly"""
    communicate = Communicate(text, voice)
    player = asyncio.subprocess.create_subprocess_exec(
        "mpv", "--no-video", "--", "fd://0",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    proc = await player
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            proc.stdin.write(chunk["data"])
            await proc.stdin.drain()
    
    if proc.stdin.can_write_eof():
        proc.stdin.write_eof()
        await proc.stdin.drain()
    await proc.wait()

def main():
    parser = argparse.ArgumentParser(description="Microsoft Edge Text-to-Speech")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # List voices command
    list_parser = subparsers.add_parser("list", help="List available voices")
    
    # Generate speech command
    generate_parser = subparsers.add_parser("generate", help="Generate speech")
    generate_parser.add_argument("--text", required=True, help="Text to speak")
    generate_parser.add_argument("--voice", default="en-US-GuyNeural", help="Voice to use")
    generate_parser.add_argument("--write-media", required=True, help="Output audio file")
    generate_parser.add_argument("--write-subtitles", help="Output subtitle file")
    
    # Playback command
    play_parser = subparsers.add_parser("play", help="Play speech immediately")
    play_parser.add_argument("--text", required=True, help="Text to speak")
    play_parser.add_argument("--voice", default="en-US-GuyNeural", help="Voice to use")
    
    args = parser.parse_args()
    
    try:
        if args.command == "list":
            asyncio.run(list_voices())
        elif args.command == "generate":
            asyncio.run(generate_speech(args.text, args.voice, args.write_media, args.write_subtitles))
        elif args.command == "play":
            asyncio.run(playback(args.text, args.voice))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()