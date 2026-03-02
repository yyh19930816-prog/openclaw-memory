#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source: https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama
# Date: 2023-10-20
# Automated AI Web Researcher using Ollama for local LLM processing

import ollama
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

class AIWebResearcher:
    def __init__(self, model: str = "llama2"):
        """Initialize with default model and research parameters"""
        self.model = model
        self.research_data = []
        self.stop_research = False
        self.max_focus_areas = 5
        self.search_depth = 2  # How many iterations of research to perform
        
    def generate_research_focus(self, query: str) -> List[Dict]:
        """Generate focus areas for research using LLM"""
        prompt = f"""Break down this research query into {self.max_focus_areas} specific focus areas, 
        each with a priority score (1-5 where 5 is most relevant). Return as a bulleted list:
        Query: {query}"""
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={'temperature': 0.7}
        )
        
        # Parse response into structured focus areas
        focus_areas = []
        for line in response['response'].split('\n'):
            if '-' in line:
                parts = line.split('-')
                if len(parts) > 1:
                    focus_areas.append({
                        'description': parts[1].strip(),
                        'priority': len(parts[1].strip().split())
                    })
                    
        return sorted(focus_areas[:self.max_focus_areas], 
                     key=lambda x: x['priority'], reverse=True)
    
    def perform_web_search(self, query: str) -> List[str]:
        """Mock web search - in reality would use search API"""
        print(f"Searching for: {query}")
        time.sleep(1)  # Simulate API delay
        # This would be replaced with actual search API calls
        return [
            f"https://example.com/{query.replace(' ', '_')}_1",
            f"https://example.com/{query.replace(' ', '_')}_2"
        ]
    
    def scrape_content(self, url: str) -> str:
        """Scrape webpage content - simplified version"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            return ' '.join(p.get_text() for p in soup.find_all('p'))
        except:
            return f"Could not retrieve content from {url}"
    
    def research_focus_area(self, focus: Dict):
        """Research a single focus area with web search and content extraction"""
        if self.stop_research:
            return
            
        queries = ollama.generate(
            model=self.model,
            prompt=f"Generate 3 search queries to research: {focus['description']}",
            options={'temperature': 0.5}
        )['response'].split('\n')[:3]
        
        for query in queries:
            if not query.strip():
                continue
                
            for url in self.perform_web_search(query):
                content = self.scrape_content(url)
                self.research_data.append({
                    'focus': focus['description'],
                    'query': query,
                    'url': url,
                    'content': content[:1000]  # Store first 1000 chars
                })
    
    def generate_summary(self, original_query: str) -> str:
        """Generate final research summary"""
        research_context = "\n".join(
            f"Focus: {item['focus']}\nContent: {item['content']}\nSource: {item['url']}"
            for item in self.research_data
        )
        
        summary = ollama.generate(
            model=self.model,
            prompt=f"Research Summary Task:\nOriginal Query: {original_query}\n\n"
                  f"Research Data:\n{research_context}\n\n"
                  "Provide a comprehensive summary answering the original query:",
            options={'temperature':