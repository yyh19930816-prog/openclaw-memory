#!/usr/bin/env python3
"""
Thumbnail Generation Utility
Source: github.com/pysnippet/thumbnails
Created: 2023-10-20
Generates video thumbnails in WebVTT or JSON format with various customization options.
"""

import os
import argparse
import subprocess
from typing import List, Optional, Union

class ThumbnailGenerator:
    """Generates thumbnails from video files in specified formats."""
    
    def __init__(self, output_format: str = 'webvtt', interval: int = 10, 
                 quality: int = 80, width: int = 320):
        """
        Initialize thumbnail generator with default settings.
        
        Args:
            output_format: webvtt or json
            interval: seconds between thumbnails
            quality: image quality (1-100)
            width: thumbnail width in pixels
        """
        self.output_format = output_format
        self.interval = interval
        self.quality = quality
        self.width = width

    def generate(self, video_path: str, output_dir: str, 
                 base_url: Optional[str] = None) -> None:
        """
        Generate thumbnails for a video file.
        
        Args:
            video_path: path to input video
            output_dir: directory to save thumbnails
            base_url: base URL for WebVTT references
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        if base_url is None:
            base_url = os.path.basename(output_dir)

        output_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir, f"{output_name}.{self.output_format}")
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps=1/{self.interval},scale={self.width}:-1',
            '-q:v', str(self.quality),
            os.path.join(output_dir, f'{output_name}_%03d.jpg')
        ]
        
        subprocess.run(cmd, check=True)
        
        if self.output_format == 'webvtt':
            self._generate_webvtt(video_path, output_path, base_url)
        elif self.output_format == 'json':
            self._generate_json(video_path, output_path, base_url)

    def _generate_webvtt(self, video_path: str, output_path: str, base_url: str) -> None:
        """Generate WebVTT file with thumbnail references."""
        duration = self._get_video_duration(video_path)
        with open(output_path, 'w') as f:
            f.write("WEBVTT\n\n")
            for i in range(0, int(duration), self.interval):
                f.write(f"{self._format_time(i)} --> {self._format_time(i + self.interval)}\n")
                f.write(f"{base_url}/{os.path.basename(video_path)}_thumb_{i:03d}.jpg\n\n")

    def _generate_json(self, video_path: str, output_path: str, base_url: str) -> None:
        """Generate JSON file with thumbnail metadata."""
        import json
        duration = self._get_video_duration(video_path)
        thumbnails = []
        for i in range(0, int(duration), self.interval):
            thumbnails.append({
                "start": i,
                "end": i + self.interval,
                "src": f"{base_url}/{os.path.basename(video_path)}_thumb_{i:03d}.jpg"
            })
        with open(output_path, 'w') as f:
            json.dump(thumbnails, f, indent=2)

    def _format_time(self, seconds: int) -> str:
        """Format seconds into hh:mm:ss.000 format."""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}.000"

    def _get_video_duration(self, video_path: str)