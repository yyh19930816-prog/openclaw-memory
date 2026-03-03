"""
ViralHook - Premium Hook Generator
Source: https://github.com/parzival1920/ViralHook---Premium-Hook-Generator
Date: 2023-11-15
Description: Python implementation of ViralHook - Premium Hook Generator for content creation
"""

import os
import random
import json
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv('.env.local')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class ViralHookGenerator:
    """
    Generates viral hooks/content ideas for social media platforms
    """
    
    def __init__(self):
        self.hook_types = [
            "Challenge-Based",
            "Controversial",
            "How-To",
            "Listicle",
            "Question-Based",
            "Shocking Fact",
            "Teaser"
        ]
        
        self.templates = {
            "Challenge-Based": [
                "Can you complete this {topic} challenge?",
                "I tried {topic} for a week - here's what happened"
            ],
            "Controversial": [
                "{topic}: Why everything you know is wrong",
                "The dark truth about {topic} no one talks about"
            ],
            "How-To": [
                "How to {action} like a pro in 3 easy steps",
                "The ultimate guide to {topic}"
            ],
            "Listicle": [
                "10 {topic} secrets experts don't want you to know",
                "5 unexpected ways {topic} can change your life"
            ],
            "Question-Based": [
                "Are you making these {topic} mistakes?",
                "What would happen if you {action} every day?"
            ],
            "Shocking Fact": [
                "{number} {topic} statistics that will blow your mind",
                "I analyzed {number} {topic} - here's what I found"
            ],
            "Teaser": [
                "This {topic} hack will change everything",
                "Wait till you see what happened when I {action}"
            ]
        }
    
    def generate_hook(self, hook_type: str, topic: str, action: str = None, number: int = None) -> str:
        """
        Generate a viral hook based on type and topic
        """
        if hook_type not in self.templates:
            raise ValueError(f"Invalid hook type. Valid types are: {', '.join(self.hook_types)}")
            
        template = random.choice(self.templates[hook_type])
        
        replacements = {
            "{topic}": topic,
            "{action}": action or "",
            "{number}": str(number) if number else ""
        }
        
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)
            
        return template
    
    def generate_multiple_hooks(self, count: int, topic: str, action: str = None) -> List[Dict]:
        """
        Generate multiple hooks of different types
        """
        hooks = []
        for _ in range(count):
            hook_type = random.choice(self.hook_types)
            if hook_type == "Shocking Fact":
                number = random.randint(5, 1000)
                hook = self.generate_hook(hook_type, topic, action, number)
            else:
                hook = self.generate_hook(hook_type, topic, action)
            
            hooks.append({
                "type": hook_type,
                "hook": hook,
                "topic": topic
            })
        
        return hooks

if __name__ == "__main__":
    # Example usage
    generator = ViralHookGenerator()
    
    print("\nViralHook Generator")
    print("-------------------")
    topic = input("Enter your topic: ")
    action = input("Enter an action (optional): ") or None
    
    hooks = generator.generate_multiple_hooks(5, topic, action)
    
    print("\nGenerated Hooks:")
    for i, hook in enumerate(hooks, 1):
        print(f"\n{i}. [{hook['type']}]: {hook['hook']}")