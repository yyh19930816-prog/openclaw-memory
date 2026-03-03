#!/usr/bin/env python3
"""
ViralHook Premium Hook Generator
Source: https://github.com/parzival1920/ViralHook---Premium-Hook-Generator
Date: 2024-03-15
Description: Python implementation of ViralHook premium content generator
"""

import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables
load_dotenv('.env.local')

app = Flask(__name__)

# Configure API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

class GeminiClient:
    """Client for interacting with Gemini API"""
    
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def generate_content(self, prompt):
        """Generate content using Gemini API"""
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.api_key}
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(
            self.BASE_URL,
            headers=headers,
            params=params,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")
            
        return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

@app.route('/')
def home():
    """Render the main interface"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_hook():
    """Generate a viral hook based on user input"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        style = data.get('style', 'casual')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
            
        # Create prompt tailored to viral hooks
        prompt = (
            f"Generate a viral {style}-style hook about '{topic}'. "
            "Make it attention-grabbing and compelling. "
            "Use curiosity gap techniques. "
            "Limit to 1-2 sentences."
        )
        
        # Generate content using Gemini
        gemini = GeminiClient(GEMINI_API_KEY)
        result = gemini.generate_content(prompt)
        
        return jsonify({'hook': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start development server
    app.run(host='0.0.0.0', port=5000, debug=True)