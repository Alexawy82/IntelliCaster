"""
Module: commentary.py

This module handles the generation of sim racing commentary using an OpenAI model.
It uses refined prompt templates (from prompt_templates.py) to build a contextual prompt
based on detected events and race context, then calls the OpenAI API to generate commentary.
"""

import time
import openai
from core import common
from . import prompt_templates

class CommentaryGenerator:
    def __init__(self):
        # Retrieve model parameters from settings; fallback to default models
        self.model = common.settings.get("commentary", "model", fallback="gpt-4-turbo-preview")
        self.temperature = float(common.settings.get("commentary", "temperature", fallback="0.7"))
    
    def generate(self, events, context):
        """
        Generate commentary text based on current race events and context.
        
        :param events: List of event dictionaries (e.g., overtakes, stops) with timestamps.
        :param context: Dictionary containing race context (e.g., league details).
        :return: Generated commentary text.
        """
        # Build a detailed prompt using the centralized template function.
        prompt = prompt_templates.get_prompt(events, context)
        messages = [
            {"role": "system", "content": "You are an energetic and insightful sim racing commentator."},
            {"role": "user", "content": prompt}
        ]
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=300
            )
            commentary_text = response.choices[0].message.content.strip()
            # Log the commentary via our common app logger.
            common.app.add_message(f"AI Commentary: {commentary_text}")
            return commentary_text
        except Exception as e:
            common.app.add_message(f"Error generating commentary: {str(e)}")
            return ""

if __name__ == "__main__":
    # For testing: simulate some events and context
    test_events = [
        {"type": "overtake", "description": "Driver A overtook Driver B", "timestamp": time.time()},
        {"type": "stopped", "description": "Driver C is stalled on track", "timestamp": time.time()}
    ]
    test_context = {"league": {"name": "Super League", "short_name": "SL"}}
    generator = CommentaryGenerator()
    print(generator.generate(test_events, test_context)) 