import requests
import os
from typing import Optional

class LLMProvider:
    def __init__(self, model_type: str = "huggingface"):
        self.model_type = model_type
        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
    async def generate(self, prompt: str) -> str:
        if self.model_type == "huggingface":
            return await self._generate_huggingface(prompt)
        return await self._generate_fallback(prompt)
    
    async def _generate_huggingface(self, prompt: str) -> str:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {self.huggingface_token}"}
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            return response.json()[0]["generated_text"]
        except Exception as e:
            print(f"Error with HuggingFace API: {e}")
            return await self._generate_fallback(prompt)
    
    async def _generate_fallback(self, prompt: str) -> str:
        # Implement basic template-based generation as fallback
        return f"Unable to generate response using LLM. Using fallback template."

# agent/prompts.py
PROMPT_TEMPLATES = {
    'architect': """You are a senior software architect. Design a system architecture for the following requirements:
    
Requirements: {task}

Focus on:
1. Component relationships
2. Technology stack
3. Design patterns
4. Scalability considerations

Response should include a Mermaid diagram and detailed explanations.""",

    'developer': """You are a senior developer. Write clean, production-ready code for the following task:
    
Task: {task}

Requirements:
1. Error handling
2. Input validation
3. Documentation
4. Best practices

Provide complete, working code with comments.""",

    'reviewer': """You are a code reviewer. Review the following implementation:
    
Implementation: {task}

Focus on:
1. Security issues
2. Performance optimizations
3. Code quality
4. Best practices

Provide specific, actionable feedback."""
}

# agent/agent.py
from .llm import LLMProvider
from .prompts import PROMPT_TEMPLATES
import asyncio

class DevAgent:
    def __init__(self):
        self.llm = LLMProvider()
        
    def _format_prompt(self, task: str, role: str) -> str:
        template = PROMPT_TEMPLATES.get(role, PROMPT_TEMPLATES['developer'])
        return template.format(task=task)
    
    async def process_task(self, task: str, role: str = 'developer') -> str:
        """Process a development task using the LLM."""
        prompt = self._format_prompt(task, role)
        response = await self.llm.generate(prompt)
        
        # Post-process the response based on role
        if role == 'architect':
            if '```mermaid' not in response:
                # Add default architecture diagram if none provided
                response = self._add_default_diagram(response, task)
        
        return response
    
    def _add_default_diagram(self, response: str, task: str) -> str:
        """Add a default architecture diagram if LLM didn't generate one."""
        default_diagram = """
```mermaid
graph TD
    A[Client] --> B[API Gateway]
    B --> C[Service Layer]
    C --> D[Database]
```
"""
        return default_diagram + "\n" + response