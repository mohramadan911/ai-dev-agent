import time
import re

class DevAgent:
    def __init__(self):
        self.responses = {
            'architect': self._generate_architecture_response,
            'developer': self._generate_development_response,
            'reviewer': self._generate_review_response
        }

    def _parse_requirements(self, task):
        """Parse key requirements from the task description."""
        # Extract key terms and requirements
        storage_terms = ['document', 'file', 'content', 'storage', 'filenet']
        auth_terms = ['user', 'auth', 'login', 'authentication']
        api_terms = ['api', 'rest', 'service', 'endpoint']
        
        requirements = {
            'needs_storage': any(term in task.lower() for term in storage_terms),
            'needs_auth': any(term in task.lower() for term in auth_terms),
            'needs_api': any(term in task.lower() for term in api_terms),
        }
        return requirements

    def _generate_architecture_response(self, task):
        """Generate dynamic architecture diagram based on task requirements."""
        reqs = self._parse_requirements(task)
        
        # Generate Mermaid diagram
        mermaid_diagram = '''graph TD
    classDef backend fill:#f9f,stroke:#333,stroke-width:2px
    classDef frontend fill:#bbf,stroke:#333,stroke-width:2px
    classDef database fill:#bfb,stroke:#333,stroke-width:2px'''
        
        components = []
        relationships = []

        # Add core components
        if 'filenet' in task.lower():
            components.extend([
                'UI[Web Interface]:::frontend',
                'API[FileNet API Layer]:::backend',
                'CPE[Content Platform Engine]:::backend',
                'DB[(Object Store)]:::database',
                'CS[Content Search]:::backend'
            ])
            relationships.extend([
                'UI --> API',
                'API --> CPE',
                'CPE --> DB',
                'CPE --> CS',
                'CS --> DB'
            ])
        else:
            components.extend([
                'UI[Web Interface]:::frontend',
                'API[Backend API]:::backend',
                'DB[(Database)]:::database'
            ])
            relationships.extend([
                'UI --> API',
                'API --> DB'
            ])

        # Add additional components based on requirements
        if reqs['needs_auth']:
            components.append('Auth[Authentication Service]:::backend')
            relationships.append('API --> Auth')

        if reqs['needs_storage']:
            components.append('Storage[(Storage Service)]:::database')
            relationships.append('API --> Storage')

        # Combine components and relationships
        mermaid_diagram += '\n    ' + '\n    '.join(components)
        mermaid_diagram += '\n    ' + '\n    '.join(relationships)

        return f"""
# System Architecture for: {task}

```mermaid
{mermaid_diagram}
```

## Component Details

1. Frontend Layer:
   - Modern React.js application
   - Responsive UI with Material Design
   - State management with Redux

2. Backend Services:
   - RESTful API with FastAPI
   - Authentication & Authorization
   - Document Management Services
   - Search & Indexing

3. Storage Layer:
   - Document Store: {', '.join(['FileNet P8', 'Object Store']) if 'filenet' in task.lower() else 'PostgreSQL'}
   - Caching: Redis
   - Search Index: Elasticsearch

## Design Patterns:
- Repository Pattern for data access
- CQRS for complex queries
- Observer Pattern for event handling
- Factory Pattern for object creation
"""

    def _generate_development_response(self, task):
        """Generate dynamic code based on task requirements."""
        reqs = self._parse_requirements(task)
        
        code_snippets = []
        
        # Add imports based on requirements
        imports = [
            "from fastapi import FastAPI, HTTPException, Depends",
            "from pydantic import BaseModel",
            "from typing import Optional, List"
        ]
        
        if reqs['needs_auth']:
            imports.append("from fastapi.security import OAuth2PasswordBearer")
        
        if 'filenet' in task.lower():
            imports.extend([
                "from filenet.core import ObjectStore, Document",
                "from filenet.constants import *"
            ])
            
        code_snippets.append('\n'.join(imports))
        
        # Add models
        if 'filenet' in task.lower():
            code_snippets.append("""
class DocumentModel(BaseModel):
    title: str
    content_type: str
    metadata: dict
    folder_path: Optional[str] = None
    
class SearchQuery(BaseModel):
    query: str
    document_class: Optional[str] = None
    max_results: Optional[int] = 50
""")
        
        # Add API endpoints
        api_code = """
app = FastAPI(title="Document Management API")

"""
        if reqs['needs_auth']:
            api_code += """
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement user verification
    return {"username": "current_user"}
"""
        
        if 'filenet' in task.lower():
            api_code += """
@app.post("/documents/", response_model=DocumentModel)
async def create_document(
    document: DocumentModel,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Initialize FileNet connection
        os = ObjectStore()
        
        # Create document
        doc = Document.create(
            class_name="Document",
            properties={
                "DocumentTitle": document.title,
                "ContentType": document.content_type,
                **document.metadata
            }
        )
        
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{doc_id}")
async def get_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        os = ObjectStore()
        doc = Document.get(doc_id)
        return {
            "id": doc_id,
            "title": doc.properties["DocumentTitle"],
            "content_type": doc.properties["ContentType"],
            "metadata": doc.properties
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Document not found")
"""
        
        code_snippets.append(api_code)
        
        return '\n'.join(code_snippets)

    def _generate_review_response(self, task):
        """Generate dynamic code review based on task context."""
        reqs = self._parse_requirements(task)
        
        review_points = [
            "## Code Quality Review\n",
            "### Security Considerations:"
        ]
        
        if reqs['needs_auth']:
            review_points.extend([
                "✅ OAuth2 implementation for authentication",
                "⚠️ Recommend adding rate limiting",
                "⚠️ Add request validation middleware"
            ])
            
        if 'filenet' in task.lower():
            review_points.extend([
                "### FileNet Specific:",
                "✅ Proper error handling for FileNet operations",
                "⚠️ Add connection pooling",
                "⚠️ Implement retry mechanism for failed operations",
                "✅ Document versioning handled correctly"
            ])
            
        review_points.extend([
            "\n### Performance:",
            "✅ Async operations used appropriately",
            "⚠️ Add caching layer",
            "⚠️ Optimize database queries"
        ])
        
        return '\n'.join(review_points)

    def process_task(self, task, role='developer'):
        """Process a development task using the specified agent role."""
        if role not in self.responses:
            raise ValueError(f"Invalid role: {role}")
        
        return self.responses[role](task)