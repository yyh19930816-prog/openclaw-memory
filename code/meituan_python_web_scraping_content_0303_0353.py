#!/usr/bin/env python3
# Source: https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama
# Date: 2023-11-15
# Automated AI Web Researcher using Ollama - Core functionality implementation

import os
import time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import ollama

class AIWebResearcher:
    def __init__(self):
        self.research_data = []
        self.research_file = "research_findings.txt"
        self.stop_command = "!stop"
        
    def generate_search_queries(self, topic: str) -> List[str]:
        """Generate search queries based on research topic"""
        prompt = f"""
        Break down this research topic into 5 specific search queries ordered by priority:
        Topic: {topic}
        Return ONLY a numbered list of search queries with no additional text.
        """
        
        response = ollama.chat(
            model='llama2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return [line.split('. ')[1] for line in response['message']['content'].split('\n') if line]

    def web_search(self, query: str) -> List[Dict]:
        """Perform web search and return relevant results"""
        # Mock search - in real implementation would use actual search API
        print(f"Searching for: {query}")
        time.sleep(1)
        return [
            {"title": "Sample Result 1", "url": "http://example.com/1", "snippet": "Sample content about the query"},
            {"title": "Sample Result 2", "url": "http://example.com/2", "snippet": "More sample content"}
        ]

    def scrape_page(self, url: str) -> str:
        """Scrape and extract text content from webpage"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return ' '.join([p.get_text() for p in soup.find_all('p')])
        except:
            return ""

    def analyze_content(self, content: str) -> str:
        """Analyze scraped content and extract relevant information"""
        prompt = f"""
        Extract the most relevant information from this content:
        {content[:2000]}... [truncated]
        Return only the key findings that relate to the research topic.
        """
        
        response = ollama.chat(
            model='llama2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

    def save_findings(self, data: dict):
        """Save research findings to file"""
        with open(self.research_file, 'a') as f:
            f.write(f"\n\n== {data['query']} ==\n")
            f.write(f"Source: {data['url']}\n")
            f.write(f"Content:\n{data['content']}\n")
            f.write("-" * 50 + "\n")

    def generate_summary(self, topic: str) -> str:
        """Generate final research summary"""
        with open(self.research_file, 'r') as f:
            content = f.read()
        
        prompt = f"""
        Based on this research content:
        {content[:10000]}... [truncated]
        
        Please provide a comprehensive summary answering this research question:
        {topic}
        """
        
        response = ollama.chat(
            model='llama2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

    def research_cycle(self, topic: str):
        """Main research workflow"""
        queries = self.generate_search_queries(topic)
        print(f"Researching: {topic}")
        print(f"Generated queries: {queries}")
        
        for query in queries:
            search_results = self.web_search(query)
            for result in search_results[:2]:  # Limit to 2 results per query
                content = self.scrape_page(result['url'])
                if content:
                    analyzed = self.analyze_content(content)
                    self.save