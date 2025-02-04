from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import time
from .prompts import AGENT_PROMPTS
from .utils import format_code

class DevAgent:
    def __init__(self):
        # Initialize Ollama with the Mistral model
        self.llm = Ollama(model="mistral")
        self.memory = ConversationBufferMemory()
        
        # Initialize different agent roles
        self.roles = {
            'architect': self._create_chain('architect'),
            'developer': self._create_chain('developer'),
            'reviewer': self._create_chain('reviewer')
        }
        
    def _create_chain(self, role):
        prompt = PromptTemplate(
            input_variables=["task"],
            template=AGENT_PROMPTS[role]
        )
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory
        )
    
    async def process_task(self, task, role='developer'):
        """Process a development task using the specified agent role."""
        if role not in self.roles:
            raise ValueError(f"Invalid role: {role}")
            
        # Simulate thinking and processing
        time.sleep(1)  # Add realistic delay
        
        response = await self.roles[role].arun(task=task)
        return format_code(response)

# src/prompts.py
AGENT_PROMPTS = {
    'architect': """You are a senior software architect. 
    Given the following task, provide a detailed technical design:
    Task: {task}
    Consider: scalability, maintainability, and best practices.
    """,
    
    'developer': """You are an expert software developer.
    Implement the following task with clean, well-documented code:
    Task: {task}
    Focus on: code quality, error handling, and documentation.
    """,
    
    'reviewer': """You are a code reviewer with high attention to detail.
    Review the following task implementation:
    Task: {task}
    Check for: bugs, security issues, and performance problems.
    """
}