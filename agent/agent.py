import time

class DevAgent:
    def __init__(self):
        self.responses = {
            'architect': self._generate_architecture_response,
            'developer': self._generate_development_response,
            'reviewer': self._generate_review_response
        }

    def _generate_architecture_response(self, task):
        """Simulate architecture planning."""
        time.sleep(1)  # Simulate thinking
        return f"""
# System Architecture for: {task}

class SystemArchitecture:
    def __init__(self):
        self.components = {{
            'frontend': 'React.js',
            'backend': 'FastAPI',
            'database': 'PostgreSQL'
        }}
        
    def design_patterns(self):
        return [
            'Repository Pattern',
            'Factory Pattern',
            'Observer Pattern'
        ]
"""

    def _generate_development_response(self, task):
        """Simulate code development."""
        time.sleep(1)  # Simulate thinking
        return f"""
# Implementation for: {task}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TaskModel(BaseModel):
    title: str
    description: str
    status: str = "pending"

@app.post("/tasks/")
async def create_task(task: TaskModel):
    return {{"status": "success", "task": task}}
"""

    def _generate_review_response(self, task):
        """Simulate code review."""
        time.sleep(1)  # Simulate thinking
        return f"""
# Code Review for: {task}

Review Comments:
1. Input Validation ✅
   - Proper use of Pydantic models
   - All required fields present

2. Error Handling ✅
   - Basic error cases covered
   - Appropriate status codes used

3. Suggestions:
   - Add request logging
   - Implement rate limiting
"""

    def process_task(self, task, role='developer'):
        """Process a development task using the specified agent role."""
        if role not in self.responses:
            raise ValueError(f"Invalid role: {role}")
        
        return self.responses[role](task)