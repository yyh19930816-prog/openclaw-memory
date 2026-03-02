#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: https://github.com/wanghaisheng/tiktoka-studio-uploader
Date: 2023-12-06
Description: Script for automating video uploads to TikTok and YouTube
"""

import os
import argparse
from datetime import datetime
from typing import Optional

class VideoUploader:
    """Core class for handling video uploads to social platforms"""
    
    def __init__(self, video_path: str, platform: str):
        self.video_path = video_path
        self.platform = platform.lower()
        self.validate_inputs()
        
    def validate_inputs(self):
        """Validate input file and platform"""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
            
        if self.platform not in ["tiktok", "youtube"]:
            raise ValueError("Platform must be either 'tiktok' or 'youtube'")
    
    def prepare_metadata(self, title: str, description: str, tags: list) -> dict:
        """Prepare video metadata dictionary"""
        return {
            'title': title,
            'description': description,
            'tags': tags,
            'upload_date': datetime.now().strftime("%Y-%m-%d"),
            'file_path': self.video_path
        }
    
    def upload_to_tiktok(self, metadata: dict) -> bool:
        """Simulate TikTok upload process"""
        print(f"Uploading to TikTok: {metadata['title']}")
        print(f"Video: {metadata['file_path']}")
        # Actual implementation would use TikTok API
        return True
        
    def upload_to_youtube(self, metadata: dict) -> bool:
        """Simulate YouTube upload process"""
        print(f"Uploading to YouTube: {metadata['title']}")
        print(f"Video: {metadata['file_path']}")
        # Actual implementation would use YouTube API
        return True
    
    def upload(self, title: str, description: str = "", tags: Optional[list] = None) -> bool:
        """Main upload method handling platform-specific uploads"""
        if tags is None:
            tags = []
            
        metadata = self.prepare_metadata(title, description, tags)
        
        if self.platform == "tiktok":
            return self.upload_to_tiktok(metadata)
        elif self.platform == "youtube":
            return self.upload_to_youtube(metadata)
        return False


def main():
    """Command line interface for the uploader"""
    parser = argparse.ArgumentParser(description="Auto upload videos to TikTok/YouTube")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("platform", choices=["tiktok", "youtube"], 
                        help="Platform to upload to")
    parser.add_argument("-t", "--title", required=True, help="Video title")
    parser.add_argument("-d", "--description", default="", help="Video description")
    parser.add_argument("--tags", nargs="+", default=[], help="List of tags")
    
    args = parser.parse_args()
    
    try:
        uploader = VideoUploader(args.video, args.platform)
        success = uploader.upload(args.title, args.description, args.tags)
        
        if success:
            print("Upload completed successfully")
        else:
            print("Upload failed")
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()