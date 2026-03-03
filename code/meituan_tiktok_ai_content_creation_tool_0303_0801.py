#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Faceless Video Generator Core Implementation
Source: github.com/jacky-xbb/faceless-video-generator
Created: 2023-11-15
Description: Core functionality for generating stories, images and videos from text input
"""

import os
import openai
import replicate
from dotenv import load_dotenv
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip
from typing import List, Dict, Optional

load_dotenv()

class FacelessGenerator:
    def __init__(self):
        # Configure API clients
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
        
        # Default configuration
        self.config = {
            "story_types": ["scary", "mystery", "motivational", "fun_facts"],
            "image_styles": ["photorealistic", "cinematic", "anime"],
            "image_size": "1024x1024",
            "fps": 24,
            "duration_per_image": 5  # seconds
        }

    def generate_story(self, story_type: str, topic: str = None) -> Dict:
        """Generate a story based on type and optional topic"""
        prompt = f"Generate a {story_type} story{f' about {topic}' if topic else ''}. "
        prompt += "Include 5-8 scenes with detailed visual descriptions for each scene."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        story_content = response.choices[0].message.content
        scenes = self._parse_story_scenes(story_content)
        return {"type": story_type, "content": story_content, "scenes": scenes}

    def _parse_story_scenes(self, story_content: str) -> List[Dict]:
        """Parse generated story into individual scenes"""
        # Simple parsing - real implementation would be more sophisticated
        scenes = []
        parts = story_content.split("\n\n")[:8]  # Get up to 8 scenes
        for i, part in enumerate(parts):
            if len(part.strip()) > 20:  # Basic length check
                scenes.append({
                    "scene_number": i + 1,
                    "description": part,
                    "subtitle": ". ".join(part.split(". ")[:2]) + "."  # First 2 sentences
                })
        return scenes

    def generate_images(self, scenes: List[Dict], style: str = "cinematic") -> List[str]:
        """Generate images for each scene using Replicate's SDXL model"""
        image_paths = []
        
        for scene in scenes:
            prompt = f"{style} style, {scene['description']}"
            
            output = self.replicate_client.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024
                }
            )
            
            image_url = output[0]
            image_path = f"scene_{scene['scene_number']}.png"
            self._download_image(image_url, image_path)
            image_paths.append(image_path)
            
        return image_paths

    def _download_image(self, url: str, save_path: str):
        """Download image from URL"""
        import requests
        response = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(response.content)

    def create_video(self, image_paths: List[str], subtitles: List[str], output_path: str = "output.mp4"):
        """Combine images and subtitles into video"""
        clips = []
        
        for img_path,