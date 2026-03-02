#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faceless Video Generator - Core Implementation
Source: https://github.com/jacky-xbb/faceless-video-generator
Created: 2023-11-15
Description: Implements story generation, image creation and video compilation
"""

import os
import json
import requests
from moviepy.editor import ImageSequenceClip, concatenate_audioclips, AudioFileClip, TextClip, CompositeVideoClip
from dotenv import load_dotenv
from openai import OpenAI
import replicate

load_dotenv()

class FacelessGenerator:
    def __init__(self):
        """Initialize API clients and basic configurations"""
        self.openai_client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_story(self, story_type="Motivational", custom_topic=None):
        """
        Generate story content using OpenAI API
        Args:
            story_type: Type of story (Motivational, Scary, etc.)
            custom_topic: Custom topic text if story_type is 'Custom Topics'
        """
        prompt = f"Generate a {story_type} story"
        if story_type == "Custom Topics" and custom_topic:
            prompt += f" about {custom_topic}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def generate_scene_images(self, story_text, style="photorealistic"):
        """
        Generate images for each scene in the story
        Args:
            story_text: Complete story text
            style: Image generation style
        """
        scenes = story_text.split("\n\n")  # Simple scene splitting
        image_paths = []
        
        for i, scene in enumerate(scenes[:3]):  # Limit to 3 scenes for demo
            prompt = f"{scene} ({style} style)"
            
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={"prompt": prompt}
            )
            
            image_url = output[0]
            img_data = requests.get(image_url).content
            path = os.path.join(self.output_dir, f"scene_{i}.jpg")
            
            with open(path, 'wb') as f:
                f.write(img_data)
            image_paths.append(path)
        
        return image_paths

    def create_video(self, image_paths, story_text, voice="male"):
        """
        Compile images and text into video with narration
        Args:
            image_paths: List of image file paths
            story_text: Story text to display as subtitles
            voice: Narration voice type
        """
        # Generate narration audio (mock implementation)
        audio_clips = []
        for i, path in enumerate(image_paths):
            audio_path = os.path.join(self.output_dir, f"audio_{i}.mp3")
            
            # In real implementation, use TTS API here
            # Mock: create silent audio clips
            silent_clip = AudioFileClip.silent(duration=5)  
            silent_clip.write_audiofile(audio_path)
            audio_clips.append(audio_path)
        
        # Create video clip
        image_clips = []
        for i, img_path in enumerate(image_paths):
            img_clip = ImageSequenceClip([img_path], durations=[5])
            
            # Add subtitles
            subtitle = TextClip(
                story_text.split("\n\n")[i],
                fontsize=24, color='white',
                size=(img_clip.size[0]-20, None),