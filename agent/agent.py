class DevAgent:
    def __init__(self):
        self.responses = {
            'architect': self._generate_architecture_response,
            'developer': self._generate_development_response,
            'reviewer': self._generate_review_response
        }

    def _parse_requirements(self, task):
        """Parse key requirements from the task description."""
        feature_terms = {
            'needs_storage': ['document', 'file', 'content', 'storage', 'upload'],
            'needs_auth': ['user', 'auth', 'login', 'authentication', 'security'],
            'needs_api': ['api', 'rest', 'service', 'endpoint', 'interface'],
            'needs_search': ['search', 'query', 'find', 'filter', 'index'],
            'needs_realtime': ['realtime', 'websocket', 'live', 'streaming'],
        }
        
        task_lower = task.lower()
        return {
            feature: any(term in task_lower for term in terms)
            for feature, terms in feature_terms.items()
        }

    def _generate_architecture_response(self, task):
        """Generate architecture diagram and description."""
        reqs = self._parse_requirements(task)
        
        # Generate Mermaid diagram
        components = ['Client[Client Application]:::frontend']
        relationships = []
        
        # Add core components based on requirements
        if reqs['needs_auth']:
            components.append('Auth[Auth Service]:::backend')
            relationships.append('Client --> Auth')
        
        if reqs['needs_api']:
            components.append('API[API Gateway]:::backend')
            relationships.append('Client --> API')
        
        if reqs['needs_storage']:
            components.extend([
                'Storage[Storage Service]:::backend',
                'DB[(Database)]:::database'
            ])
            relationships.extend([
                'API --> Storage',
                'Storage --> DB'
            ])
        
        if reqs['needs_search']:
            components.append('Search[Search Engine]:::backend')
            relationships.append('API --> Search')

        # Build Mermaid diagram
        mermaid = f"""graph TD
    classDef frontend fill:#bbf,stroke:#333,stroke-width:2px
    classDef backend fill:#f9f,stroke:#333,stroke-width:2px
    classDef database fill:#bfb,stroke:#333,stroke-width:2px
    
    {chr(10) + '    '.join(components)}
    {chr(10) + '    '.join(relationships)}"""

        return f"""
# System Architecture for: {task}

```mermaid
{mermaid}
```

## Component Details

1. Frontend Layer:
   - Modern SPA using React.js
   - Material UI components
   - Redux state management

2. Backend Services:
   - {self._get_backend_services(reqs)}

3. Storage Layer:
   - {self._get_storage_details(reqs)}

## Design Patterns:
- Repository Pattern for data access
- Factory Pattern for service creation
- Observer Pattern for event handling
"""

    def _generate_development_response(self, task):
        """Generate code implementation."""
        reqs = self._parse_requirements(task)
        
        imports = [
            "from fastapi import FastAPI, HTTPException, Depends",
            "from pydantic import BaseModel",
            "from typing import Optional, List"
        ]
        
        if reqs['needs_auth']:
            imports.append("from fastapi.security import OAuth2PasswordBearer")
        
        code = f"""
# Implementation for: {task}

{chr(10).join(imports)}

{self._generate_models(reqs)}

{self._generate_api_endpoints(reqs)}
"""
        return code

    def _generate_review_response(self, task):
        """Generate code review feedback."""
        reqs = self._parse_requirements(task)
        
        review_points = ["## Code Review Feedback\n"]
        
        if reqs['needs_auth']:
            review_points.extend([
                "### Security:",
                "✅ Authentication implementation",
                "⚠️ Add rate limiting",
                "⚠️ Implement request validation"
            ])
        
        if reqs['needs_storage']:
            review_points.extend([
                "\n### Data Handling:",
                "✅ Proper error handling",
                "⚠️ Add connection pooling",
                "⚠️ Implement caching strategy"
            ])
        
        review_points.extend([
            "\n### Performance:",
            "✅ Async operations used appropriately",
            "⚠️ Optimize database queries",
            "⚠️ Add monitoring and logging"
        ])
        
        return '\n'.join(review_points)

    def _get_backend_services(self, reqs):
        services = ["RESTful API with FastAPI"]
        if reqs['needs_auth']:
            services.append("JWT Authentication")
        if reqs['needs_storage']:
            services.append("File Management Service")
        if reqs['needs_search']:
            services.append("Search Service with Elasticsearch")
        return '\n   - '.join(services)

    def _get_storage_details(self, reqs):
        if reqs['needs_storage']:
            return """PostgreSQL for metadata
   - S3 for file storage
   - Redis for caching"""
        return "PostgreSQL for application data"

    def _generate_models(self, reqs):
        models = []
        if reqs['needs_storage']:
            models.append("""
class FileModel(BaseModel):
    filename: str
    content_type: str
    size: int
    metadata: Optional[dict] = None""")
        
        if reqs['needs_auth']:
            models.append("""
class User(BaseModel):
    username: str
    email: str
    disabled: Optional[bool] = None""")
        
        return '\n'.join(models)

    def _generate_api_endpoints(self, reqs):
        endpoints = ["app = FastAPI(title='API Service')"]
        
        if reqs['needs_auth']:
            endpoints.append("""
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implement authentication logic
    pass""")
        
        if reqs['needs_storage']:
            endpoints.append("""
@app.post("/upload/")
async def upload_file(file: FileModel):
    try:
        # Implement file upload logic
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))""")
        
        return '\n'.join(endpoints)

    def process_task(self, task, role='developer'):
        """Process a development task using the specified agent role."""
        if role not in self.responses:
            raise ValueError(f"Invalid role: {role}")
        
        return self.responses[role](task)