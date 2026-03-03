#!/usr/bin/env python3
# source: jacky-xbb/faceless-video-generator
# date: 2023-11-15
# Faceless Video Generator - Core functionality implementation with story generation, image creation, and video compilation

import os
import json
import requests
from typing import List, Dict
from openai import OpenAI
import replicate
from dotenv import load_dotenv
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Load environment variables
load_dotenv()

class FacelessVideoGenerator:
    def __init__(self):
        """Initialize generator with API clients and configurations"""
        self.openai_client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        self.story_types = [
            "Scary", "Mystery", "Bedtime", "History", 
            "Urban Legends", "Motivational", "Fun Facts"
        ]
        self.image_styles = [
            "photorealistic", "cinematic", "anime",
            "comic-book", "pixar-art"
        ]
        
    def generate_story(self, story_type: str, theme: str = None) -> Dict:
        """Generate story content using OpenAI API
        
        Args:
            story_type: Type of story from predefined options
            theme: Optional custom theme/topic
            
        Returns:
            Dictionary containing story metadata and scenes
        """
        prompt = f"Generate a {story_type} story{f' about {theme}' if theme else ''}. "
        prompt += "Provide as JSON with title, scenes (list with scene_description), "
        prompt += "and summary. Each scene should be visualizable."
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_images(self, scenes: List[str], style: str = "cinematic") -> List[str]:
        """Generate images for each scene using Replicate API
        
        Args:
            scenes: List of scene descriptions
            style: Visual style for generated images
            
        Returns:
            List of image URLs for each scene
        """
        image_urls = []
        model = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
        
        for scene in scenes:
            output = replicate.run(
                model,
                input={
                    "prompt": f"{scene}, {style} style",
                    "width": 1024,
                    "height": 576
                }
            )
            image_urls.append(output[0])
            
        return image_urls
    
    def download_images(self, urls: List[str], output_dir: str = "temp_images"):
        """Download images from URLs to local directory
        
        Args:
            urls: List of image URLs
            output_dir: Directory to save images
        """
        os.makedirs(output_dir, exist_ok=True)
        for i, url in enumerate(urls):
            response = requests.get(url)
            with open(f"{output_dir}/scene_{i}.jpg", "wb") as f:
                f.write(response.content)
    
    def create_video(self, story: Dict, image_dir: str, output_path: str = "output.mp4"):
        """Create video from story scenes and images
        
        Args:
            story: Story dictionary with scenes and text
            image_dir: Directory containing scene images
            output_path: Path to save final video
        """
        clips = []
        duration_per_scene = 5  # seconds
        
        for i, scene in enumerate(story["scenes"]):
            # Create image clip
            img_clip = ImageClip(f"{image_dir}/scene_{i}.