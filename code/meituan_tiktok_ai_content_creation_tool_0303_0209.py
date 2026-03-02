# faceless_video_generator.py
# Source: jacky-xbb/faceless-video-generator (https://github.com/jacky-xbb/faceless-video-generator)
# Date: 2023-11-15
# This script provides core functionality for generating faceless videos including story generation, image creation and video compilation

import os
import openai
import replicate
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class FacelessVideoGenerator:
    def __init__(self):
        """Initialize the generator with API configurations"""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_BASE_URL")
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        
        # Story types supported by the generator
        self.story_types = [
            "scary", "mystery", "bedtime", "history", 
            "urban_legend", "motivational", "fun_facts",
            "jokes", "life_tips", "philosophy", "love", "custom"
        ]
        
        # Style options for image generation
        self.image_styles = [
            "photorealistic", "cinematic", "anime",
            "comic-book", "pixar-art"
        ]

    def generate_story(self, story_type: str, custom_topic: Optional[str] = None) -> Dict:
        """Generate a story using OpenAI's API
        
        Args:
            story_type: Type of story to generate (must be in self.story_types)
            custom_topic: Optional topic for custom story types
            
        Returns:
            Dictionary containing story data including title, content and scenes
        """
        if story_type not in self.story_types:
            raise ValueError(f"Invalid story type. Must be one of: {self.story_types}")
            
        prompt = f"Generate a {story_type} story"
        if story_type == "custom" and custom_topic:
            prompt += f" about {custom_topic}"
            
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        story_content = response.choices[0].message.content
        scenes = story_content.split('\n\n')  # Simple scene splitting
        
        return {
            "title": f"{story_type.capitalize()} Story",
            "content": story_content,
            "scenes": scenes
        }

    def generate_image(self, prompt: str, style: str = "photorealistic") -> str:
        """Generate an image for a story scene using Replicate
        
        Args:
            prompt: Text description of the image to generate
            style: Visual style for the image
            
        Returns:
            URL of the generated image
        """
        if style not in self.image_styles:
            raise ValueError(f"Invalid style. Must be one of: {self.image_styles}")
            
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": f"{style} style, {prompt}",
                "width": 1024,
                "height": 576  # 16:9 aspect ratio for videos
            }
        )
        return output[0]  # Returns the image URL

    def create_video(self, scenes: List[str], images: List[str], output_path: str = "output.mp4"):
        """Combine scenes (as text) and images into a video
        
        Args:
            scenes: List of text scenes (subtitles)
            images: List of image URLs or file paths
            output_path: Path to save the final video
        """
        if len(scenes) != len(images):
            raise ValueError