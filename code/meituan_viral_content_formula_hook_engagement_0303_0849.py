#!/usr/bin/env python3
# Source: https://github.com/parzival1920/ViralHook---Premium-Hook-Generator
# Date: 2024-02-20
# Description: Python implementation of ViralHook - A premium hook generator

import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables from .env.local
load_dotenv('.env.local')

app = Flask(__name__)

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def generate_hook(prompt):
    """Generate marketing hook using Gemini API"""
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Generate a viral marketing hook about: {prompt}. "
                        "Make it catchy, under 200 characters, and include "
                        "emotive language."
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        generated_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return generated_text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle hook generation requests"""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
            
        hook = generate_hook(prompt)
        
        if not hook:
            return jsonify({"error": "Failed to generate hook"}), 500
            
        return jsonify({"hook": hook})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check if API key is set
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in .env.local")
        exit(1)
        
    app.run(debug=True, port=3000)