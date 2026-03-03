#!/usr/bin/env python3
# Source: https://github.com/IgorShadurin/app.yumcut.com
# Date: 2023-11-20
# YumCut: AI-powered short video generator for social platforms

import os
import random
from typing import List, Dict
import moviepy.editor as mpy
from moviepy.video.tools.segmenting import find_objects
from moviepy.video.fx import resize, fadein, fadeout
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import openai

class YumCutGenerator:
    """Core video generator class for creating short-form vertical videos"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.font_path = "assets/fonts/Roboto-Bold.ttf"
        self.max_duration = 59  # Max duration for shorts
        
        # Initialize APIs
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_script(self, topic: str) -> str:
        """Generates video script using GPT-3"""
        prompt = f"""Write a short engaging script for a 30-60 second TikTok/Shorts video about {topic}. 
        Use simple language, emojis and hooks optimized for retention."""
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    
    def text_to_speech(self, text: str, language: str = "en") -> str:
        """Converts text to speech and saves audio file"""
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = os.path.join(self.output_dir, "voiceover.mp3")
        tts.save(audio_path)
        return audio_path
    
    def generate_captions(self, script: str) -> List[Dict]:
        """Creates timed captions for video"""
        words = script.split()
        chunk_size = len(words) // 5
        captions = []
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            captions.append({
                "text": chunk,
                "start": i * 0.3,
                "end": (i + chunk_size) * 0.3
            })
        return captions
    
    def create_video(self, script: str, style: str = "modern") -> str:
        """Main pipeline: generates full video from script"""
        # Generate voiceover
        audio_path = self.text_to_speech(script)
        audio = mpy.AudioFileClip(audio_path)
        
        # Adjust duration if needed
        duration = min(audio.duration, self.max_duration)
        
        # Get captions
        captions = self.generate_captions(script)
        
        # Generate video clips
        clips = []
        for i in range(int(duration)):
            bg_color = self._get_style_color(style)
            img = Image.new("RGB", (1080, 1920), bg_color)
            draw = ImageDraw.Draw(img)
            font_size = 50 if style == "minimal" else 70
            
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except:
                font = ImageFont.load_default()
                
            text = captions[min(i, len(captions)-1)]["text"]
            draw.text((540, 960), text, font=font, fill="white", anchor="mm")
            
            frame_path = os.path.join(self.output_dir, f"frame_{i}.jpg")
            img.save(frame_path)
            clips.append(mpy.ImageClip(frame_path).set_duration(1))
        
        # Combine clips and add audio
        video = mpy.concatenate_videoclips(clips)
        video = video.set_audio(audio)
        video = video.resize