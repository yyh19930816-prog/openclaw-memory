#!/usr/bin/env python3
# Source: https://github.com/pysnippet/thumbnails
# Date: 2023-04-01
# Description: Generate video thumbnails with WebVTT/JSON output options

import os
import argparse
import subprocess
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

@dataclass
class ThumbnailConfig:
    input_path: str
    base_url: str = "/media/"
    output_dir: str = "thumbnails/"
    interval: int = 5
    format: str = "webvtt"
    quality: int = 80

class ThumbnailGenerator:
    def __init__(self, config: ThumbnailConfig):
        self.config = config
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)

    def generate(self) -> None:
        """Generate thumbnails for video file"""
        if os.path.isdir(self.config.input_path):
            self._process_directory()
        else:
            self._process_file(self.config.input_path)

    def _process_directory(self) -> None:
        """Process all video files in directory"""
        for root, _, files in os.walk(self.config.input_path):
            for file in files:
                if self._is_video_file(file):
                    self._process_file(os.path.join(root, file))

    def _process_file(self, input_file: str) -> None:
        """Process single video file"""
        video_id = Path(input_file).stem
        output_prefix = os.path.join(self.config.output_dir, video_id)
        
        # Get video duration
        duration = self._get_video_duration(input_file)
        if not duration:
            return
            
        # Generate thumbnails and metadata
        thumbnails = self._generate_thumbnails(input_file, output_prefix, duration)
        self._generate_metadata(video_id, thumbnails)

    def _get_video_duration(self, input_file: str) -> Optional[float]:
        """Get video duration using ffprobe"""
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except (subprocess.SubprocessError, ValueError):
            return None

    def _generate_thumbnails(self, input_file: str, output_prefix: str, duration: float) -> List[Dict]:
        """Generate thumbnail images at intervals"""
        thumbnails = []
        time = 0.0
        
        while time <= duration:
            thumb_path = f"{output_prefix}_{int(time)}.jpg"
            cmd = [
                "ffmpeg",
                "-ss", str(time),
                "-i", input_file,
                "-vframes", "1",
                "-q:v", str(self.config.quality),
                "-vf", "scale=-1:240",
                thumb_path
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                thumbnails.append({
                    "time": time,
                    "url": os.path.join(self.config.base_url, os.path.basename(thumb_path))
                })
            except subprocess.SubprocessError:
                pass
            time += self.config.interval
            
        return thumbnails

    def _generate_metadata(self, video_id: str, thumbnails: List[Dict]) -> None:
        """Generate WebVTT or JSON metadata file"""
        output_file = os.path.join(self.config.output_dir, f"{video_id}.{self.config.format}")
        
        if self.config.format == "webvtt":
            with open(output_file, "w") as f:
                f.write("WEBVTT\n\n")
                for thumb in thumbnails:
                    start = timedelta(seconds=thumb["time"])
                    f.write(f"{start}.000 --> {start + timedelta(seconds=1)}.000