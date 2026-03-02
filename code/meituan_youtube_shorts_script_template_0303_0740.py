#!/usr/bin/env python3
# Source: https://github.com/IgorShadurin/app.yumcut.com
# Date: 2023-11-20
# Description: Core implementation of YumCut - open-source AI short video generator

import os
import random
from moviepy.editor import *
from openai import OpenAI
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

class YumCutGenerator:
    def __init__(self, openai_key):
        """Initialize generator with API keys"""
        self.openai = OpenAI(api_key=openai_key)
        self.output_dir = "output_videos"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_script(self, topic, style="informative"):
        """
        Generate video script using GPT-3.5
        Returns: Generated text script
        """
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {style} short video script writer."},
                {"role": "user", "content": f"Create a 15-30 second script about: {topic}"}
            ]
        )
        return response.choices[0].message.content

    def text_to_speech(self, text, lang="en"):
        """Convert text to speech audio file"""
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_path = os.path.join(self.output_dir, "voiceover.mp3")
        tts.save(audio_path)
        return audio_path

    def generate_images(self, script, num_images=3):
        """
        Generate AI images based on script key moments
        Returns: List of image file paths
        """
        image_prompts = self._extract_key_moments(script)
        image_paths = []
        
        for i, prompt in enumerate(image_prompts[:num_images]):
            response = self.openai.images.generate(
                prompt=f"{prompt} in minimalist digital art style",
                n=1,
                size="512x512"
            )
            img_url = response.data[0].url
            img_path = os.path.join(self.output_dir, f"frame_{i}.jpg")
            self._download_image(img_url, img_path)
            image_paths.append(img_path)
        
        return image_paths

    def create_video(self, audio_path, image_paths, output_name="final_video"):
        """Compile final video with images and audio"""
        # Create image clips with captions
        clips = []
        audio_clip = AudioFileClip(audio_path)
        
        # Calculate duration per image
        duration = audio_clip.duration / len(image_paths)
        
        for img_path in image_paths:
            img = ImageClip(img_path).set_duration(duration)
            img = img.resize(height=1920)  # Vertical format
            clips.append(img)
        
        # Combine all elements
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio_clip)
        
        # Export final video
        output_path = os.path.join(self.output_dir, f"{output_name}.mp4")
        video.write_videofile(output_path, fps=24)
        return output_path

    def _extract_key_moments(self, text):
        """Helper to identify key moments from script"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return sentences[:3]  # Use first 3 sentences as key moments

    def _download_image(self, url, save_path):
        """Helper to download image from URL"""
        import requests
        response = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(response.content)

if __name__ == "__main__":
    # Example usage
    generator = YumCutGenerator(openai_key="your-openai-key-here")
    
    # Step 1: Generate script
    script = generator.generate_script("The future of AI in daily life")
    print