#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Source: https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama
# Date: 2023-11-15
# Automated AI Web Researcher using Ollama LLM

import os
import time
import requests
from bs4 import BeautifulSoup
import ollama

class AIWebResearcher:
    def __init__(self, model="mistral"):
        self.model = model
        self.research_data = []
        self.output_file = "research_findings.txt"
        
    def generate_search_queries(self, topic):
        """Generate priority search queries from the research topic"""
        prompt = f"""
        Given the research topic: '{topic}'
        Generate 5 specific research focus areas with priorities (1-5, 1=highest).
        Format as numbered lines with priority first, then focus area.
        Example:
        1 The predicted year global population will peak
        2 Factors influencing global population trends
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        queries = [
            line.split(" ", 1)[1].strip() 
            for line in response["response"].split("\n") 
            if line.strip()
        ]
        return queries
    
    def perform_web_search(self, query):
        """Mock web search function - replace with actual search API"""
        print(f"Searching: {query}")
        time.sleep(1)  # Simulate search delay
        return [
            {"title": f"Example result for {query}", "url": "https://example.com/page1"},
            {"title": f"Another result for {query}", "url": "https://example.com/page2"}
        ]
    
    def scrape_page(self, url):
        """Scrape content from webpage"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
            return text[:2000]  # Limit to first 2000 chars
        except:
            return None
    
    def research_focus_area(self, focus_area):
        """Research a single focus area"""
        search_results = self.perform_web_search(focus_area)
        
        for result in search_results:
            content = self.scrape_page(result["url"])
            if content:
                self.research_data.append({
                    "focus": focus_area,
                    "url": result["url"],
                    "content": content
                })
                self.save_to_file(focus_area, result["url"], content)
    
    def save_to_file(self, focus, url, content):
        """Save research findings to file"""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== RESEARCH FOCUS: {focus} ===\n")
            f.write(f"Source URL: {url}\n")
            f.write(f"Content:\n{content}\n")
    
    def generate_summary(self, original_topic):
        """Generate final summary from collected research"""
        research_text = "\n".join(
            f"Focus: {item['focus']}\nURL: {item['url']}\nContent: {item['content'][:500]}..."
            for item in self.research_data
        )
        
        prompt = f"""
        Based on this research about '{original_topic}':
        {research_text}
        
        Provide a comprehensive summary answering the original question.
        Include key findings and sources.
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return response["response"]
    
    def interactive_mode(self, original_topic):
        """Allow user to ask questions about research"""
        print("\nEntering interactive mode. Type 'exit' to quit.")
        
        while True:
            question = input("\nAsk about the research: ")
            if question.lower() == 'exit':
                break
                
            prompt = f"""
            Research topic: {original_topic}
            Research data: {self.research_data}
            
            Question: {question}
            Answer based on the research findings.
            """