"""
ViralHook Hook Generator Implementation
Source: github.com/parzival1920/ViralHook---Premium-Hook-Generator
Date: 2023-11-15
Description: Python implementation of ViralHook's AI-powered hook generator
"""

import os
import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

class ViralHookGenerator:
    """Core hook generation logic using Gemini API"""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def generate_hook(self, topic: str, style: Optional[str] = "viral") -> str:
        """Generate a hook based on topic and style"""
        if not self.api_key:
            raise ValueError("Gemini API key not set")
            
        prompt = f"""
        Generate a catchy {style}-style hook about {topic}.
        Make it attention-grabbing and under 280 characters.
        Include emojis where appropriate.
        """
        
        params = {"key": self.api_key}
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        try:
            response = requests.post(
                self.base_url,
                params=params,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Error generating hook: {str(e)}"

class HookServer(BaseHTTPRequestHandler):
    """Simple HTTP server to serve generated hooks"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith("/generate"):
            params = self.path.split("?")[1] if "?" in self.path else ""
            query = dict(q.split("=") for q in params.split("&") if "=" in q)
            
            topic = query.get("topic", "")
            style = query.get("style", "viral")
            
            if not topic:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Topic parameter required")
                return
                
            hook = generator.generate_hook(topic, style)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"hook": hook}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    # Load API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        exit(1)
        
    generator = ViralHookGenerator(api_key)
    
    # Example usage
    print("Sample hook:", generator.generate_hook("AI in marketing"))
    
    # Start server
    server_addr = ("", 8080)
    httpd = HTTPServer(server_addr, HookServer)
    print("Server running at http://localhost:8080")
    httpd.serve_forever()