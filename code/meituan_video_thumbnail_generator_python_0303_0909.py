#!/usr/bin/env python3
# Source: https://github.com/pysnippet/thumbnails
# Date: 2023-03-15
# Video thumbnail generator supporting WebVTT and JSON outputs

import os
import argparse
import subprocess
from glob import glob
from pathlib import Path
from typing import Optional, List, Tuple, Union

class ThumbnailGenerator:
    """Generate video thumbnails with WebVTT or JSON metadata output."""
    
    def __init__(self, 
                 output_dir: str = "thumbnails",
                 interval: int = 10,
                 format: str = "webvtt",
                 quality: int = 85,
                 width: int = 320):
        """
        Initialize thumbnail generator with output settings.
        
        Args:
            output_dir: Directory to save thumbnails and metadata
            interval: Seconds between thumbnails
            format: Output format ('webvtt' or 'json')
            quality: JPEG quality (1-100)
            width: Thumbnail width (height auto-scales)
        """
        self.output_dir = Path(output_dir)
        self.interval = interval
        self.format = format.lower()
        self.quality = quality
        self.width = width
        
        self.output_dir.mkdir(exist_ok=True)
    
    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds using ffprobe."""
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 
            'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
            return float(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get video duration: {e}")
    
    def _generate_thumbnail(self, video_path: str, timestamp: int) -> str:
        """Generate single thumbnail at specified timestamp."""
        filename = f"{Path(video_path).stem}_{timestamp}s.jpg"
        output_path = self.output_dir / filename
        
        cmd = [
            'ffmpeg', '-ss', str(timestamp), '-i', str(video_path),
            '-vframes', '1', '-q:v', str(self.quality),
            '-vf', f'scale={self.width}:-1', str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return str(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate thumbnail: {e}")
    
    def _generate_webvtt(self, thumbnails: List[Tuple[int, str]]) -> str:
        """Generate WebVTT metadata file."""
        vtt_path = self.output_dir / "thumbnails.vtt"
        with open(vtt_path, 'w') as f:
            f.write("WEBVTT\n\n")
            for start, path in thumbnails:
                name = Path(path).name
                f.write(f"{start}.000 --> {start + self.interval}.000\n")
                f.write(f"{name}\n\n")
        return str(vtt_path)
    
    def _generate_json(self, thumbnails: List[Tuple[int, str]]) -> str:
        """Generate JSON metadata file."""
        import json
        json_path = self.output_dir / "thumbnails.json"
        data = {
            "width": self.width,
            "interval": self.interval,
            "thumbnails": [
                {"start": start, "url": Path(path).name} 
                for start, path in thumbnails
            ]
        }
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        return str(json_path)
    
    def generate(self, video_path: str) -> dict:
        """
        Generate thumbnails for a video file.
        
        Returns:
            Dictionary with paths to generated files
        """
        duration =