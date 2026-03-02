#!/usr/bin/env python3
# Source: https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama
# Date: 2024-03-15
# Automated AI Web Researcher using Ollama LLM

import os
import time
import requests
from bs4 import BeautifulSoup
import ollama

class AIWebResearcher:
    def __init__(self):
        self.research_data = []
        self.search_depth = 2  # Controls how many rounds of research to perform
        self.stop_command = "!stop"
    
    def get_user_query(self):
        """Get research topic/question from user"""
        print("Enter your research question/topic (or '{}' to stop):".format(self.stop_command))
        return input("> ").strip()
    
    def generate_focus_areas(self, query):
        """Use LLM to generate research focus areas"""
        prompt = f"""
        Analyze this research query and generate 5 specific focus areas with priorities:
        Query: {query}
        
        Respond in format:
        1. [Priority] [Focus Area]
        2. [Priority] [Focus Area]
        ...
        """
        response = ollama.generate(model='llama2', prompt=prompt)
        return self._parse_focus_areas(response['response'])
    
    def _parse_focus_areas(self, llm_output):
        """Parse LLM response into focus areas"""
        areas = []
        for line in llm_output.split('\n'):
            if line.strip() and line[0].isdigit():
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    areas.append((int(parts[1]), parts[2]))
        return sorted(areas, reverse=True)
    
    def search_web(self, query):
        """Simulate web search (replace with actual search API)"""
        print(f"Searching for: {query}")
        # Mock implementation - real version would use APIs
        mock_results = [
            f"https://example.com/{query.replace(' ', '_')}_1",
            f"https://example.com/{query.replace(' ', '_')}_2"
        ]
        return mock_results[:2]  # Return first 2 results
    
    def scrape_content(self, url):
        """Scrape content from webpage"""
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
            return text[:1000]  # Return first 1000 chars
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
    
    def research_cycle(self, focus_areas):
        """Perform research on each focus area"""
        for priority, area in focus_areas:
            print(f"\nResearching priority {priority}: {area}")
            search_results = self.search_web(area)
            
            for url in search_results:
                content = self.scrape_content(url)
                if content:
                    self.research_data.append({
                        'focus_area': area,
                        'url': url,
                        'content': content
                    })
                    print(f"Found content at {url}")
    
    def generate_summary(self, original_query):
        """Generate final summary using LLM"""
        research_context = "\n\n".join(
            f"Focus: {item['focus_area']}\nURL: {item['url']}\nContent: {item['content']}"
            for item in self.research_data
        )
        
        prompt = f"""
        Original Query: {original_query}
        
        Research Findings:
        {research_context}
        
        Generate a comprehensive summary answering the original query.
        """
        response = ollama.generate(model='llama2', prompt=prompt)
        return response['response']
    
    def run(self):
        """Main execution loop"""
        query = self.get_user_query()
        if query.lower() == self.stop_command:
            return
        
        focus_areas = self.generate_focus_areas(query)
        print("\nGenerated Focus Areas:")
        for pri, area in focus_areas:
            print(f"{pri}: {area}")