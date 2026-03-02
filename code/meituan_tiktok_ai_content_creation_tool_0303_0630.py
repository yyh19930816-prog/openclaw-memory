# Source: github.com/jacky-xbb/faceless-video-generator
# Date: 2024-04-15
# Description: Faceless video generator implementing story, image generation and video compilation

import os
import openai
import replicate
import random
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from dotenv import load_dotenv
from typing import List, Dict, Tuple

# Load environment variables
load_dotenv()

class FacelessVideoGenerator:
    """Main class for generating faceless videos"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
        self.story_types = [
            "Scary", "Mystery", "Bedtime", "Interesting History", 
            "Urban Legends", "Motivational", "Fun Facts", 
            "Long Form Jokes", "Life Pro Tips", "Philosophy", 
            "Love", "Custom"
        ]
        self.image_styles = [
            "photorealistic", "cinematic", "anime", 
            "comic-book", "pixar-art"
        ]
        
    def generate_story(self, story_type: str, custom_topic: str = None) -> Tuple[str, List[str]]:
        """Generate story text and scene descriptions"""
        prompt = f"Write a {story_type} story"
        if custom_topic:
            prompt += f" about {custom_topic}"
            
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a storytelling assistant."},
                {"role": "user", "content": f"{prompt}. First generate the full story text, then list 5 vivid scene descriptions for image generation."}
            ]
        )
        
        full_text = response.choices[0].message.content
        scenes = self._extract_scenes(full_text)
        return full_text, scenes
        
    def _extract_scenes(self, text: str) -> List[str]:
        """Helper to extract scene descriptions from GPT response"""
        scenes = []
        lines = text.split('\n')
        
        for line in lines:
            if "scene" in line.lower() or "description" in line.lower():
                scenes.append(line.strip())
                if len(scenes) >= 5:
                    break
                    
        return scenes if scenes else ["Create an image representing this story"] * 5
        
    def generate_image(self, prompt: str, style: str = "photorealistic") -> str:
        """Generate image using Replicate API"""
        prompt = f"{style} style, {prompt}"
        
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "negative_prompt": "blurry, low quality",
                "width": 1024,
                "height": 576
            }
        )
        return output[0]
        
    def create_video(self, images: List[str], text: str, output_path: str = "output.mp4") -> None:
        """Combine images and text into video"""
        clips = []
        
        # Create image clips (5 sec each)
        for img_path in images:
            clip = ImageClip(img_path).set_duration(5)
            clips.append(clip)
            
        # Add subtitles
        subtitles = [((i*5, (i+1)*5), line) for i, line in enumerate(text.split('. ')[:5])]
        generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white', bg_color='black')