#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faceless Video Generator Core Script
Source: https://github.com/jacky-xbb/faceless-video-generator
Date: 2023-11-15
Description: Core functionality for generating faceless videos including story generation,
             image creation, and video compilation with subtitles.
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
import openai
import replicate
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip

# Load environment variables
load_dotenv()

class FacelessVideoGenerator:
    """Main class handling faceless video generation workflow."""
    
    def __init__(self):
        self.configure_apis()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def configure_apis(self):
        """Configure required API connections."""
        openai.api_base = os.getenv("OPENAI_BASE_URL")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
        
    def generate_story(self, story_type: str, custom_topic: str = None) -> Dict:
        """Generate story using OpenAI API based on type."""
        prompt_templates = {
            "scary": "Write a scary story suitable for faceless video (400-500 words).",
            "motivational": "Write an inspirational motivational story (400-500 words).",
            "custom": f"Write a detailed story about: {custom_topic} (400-500 words)."
        }
        
        prompt = prompt_templates.get(story_type.lower(), prompt_templates["custom"])
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "title": f"Generated {story_type} Story",
            "content": response.choices[0].message.content,
            "scenes": self._split_into_scenes(response.choices[0].message.content)
        }
    
    def _split_into_scenes(self, content: str, scene_length: int = 80) -> List[str]:
        """Split story content into manageable scenes."""
        words = content.split()
        return [' '.join(words[i:i+scene_length]) for i in range(0, len(words), scene_length)]
    
    def generate_images(self, scenes: List[str], style: str = "cinematic") -> List[str]:
        """Generate images for each scene using Replicate API."""
        image_paths = []
        
        model = "stability-ai/sdxl:c221b2b8ef527988fb59bf24a8b97c4561f1c671f73bd389f866bfb27c061316"
        style_prompt = {
            "cinematic": "cinematic still, ultra-detailed, visually stunning",
            "anime": "Studio Ghibli anime style, beautiful illustration",
            "photorealistic": "ultra-realistic photography, 8k resolution"
        }.get(style, "high quality digital art")
        
        for i, scene in enumerate(scenes):
            output = replicate.run(
                model,
                input={
                    "prompt": f"{style_prompt}, {scene}",
                    "negative_prompt": "text, watermark, signature",
                    "width": 1024,
                    "height": 576
                }
            )
            image_path = self.output_dir / f"scene_{i}.png"
            self._download_image(output[0], image_path)
            image_paths.append(str(image_path))
            
        return image_paths
    
    def _download_image(self, url: str, save_path: Path):
        """Download image from URL."""
        import requests
        response = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(response.content)
    
    def create_video(self, image_paths: List