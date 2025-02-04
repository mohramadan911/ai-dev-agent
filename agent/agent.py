import re
from typing import Dict, List

class DevAgent:
    def __init__(self):
        self.responses = {
            'architect': self._generate_architecture_response,
            'developer': self._generate_development_response,
            'reviewer': self._generate_review_response
        }
        
    def _extract_technologies(self, task: str) -> Dict[str, List[str]]:
        """Extract specific technologies mentioned in the task."""
        tech_categories = {
            'frontend': ['react', 'angular', 'vue', 'jquery', 'bootstrap'],
            'backend': ['node', 'python', 'java', 'fastapi', 'spring', 'django'],
            'database': ['mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'kubernetes', 'docker'],
            'cms': ['filenet', 'sharepoint', 'documentum', 'alfresco']
        }
        
        found_tech = {category: [] for category in tech_categories}
        task_lower = task.lower()
        
        for category, technologies in tech_categories.items():
            found_tech[category] = [tech for tech in technologies if tech in task_lower]
            
        return found_tech
        
    def _parse_requirements(self, task: str) -> Dict[str, bool]:
        """Enhanced requirement parsing with more specific features."""
        feature_terms = {
            'needs_storage': ['document', 'file', 'content', 'storage', 'upload'],
            'needs_auth': ['user', 'auth', 'login', 'authentication', 'security'],
            'needs_api': ['api', 'rest', 'service', 'endpoint', 'interface'],
            'needs_search': ['search', 'query', 'find', 'filter', 'index'],
            'needs_realtime': ['realtime', 'websocket', 'live', 'streaming'],
            'needs_workflow': ['workflow', 'process', 'approval', 'routing'],
            'needs_integration': ['integrate', 'connect', 'third-party', 'external']
        }
        
        task_lower = task.lower()
        return {
            feature: any(term in task_lower for term in terms)
            for feature, terms in feature_terms.items()
        }

    def _generate_architecture_response(self, task: str) -> str:
        """Generate a more specific architecture response based on task analysis."""
        reqs = self._parse_requirements(task)
        tech = self._extract_technologies(task)
        
        # Build dynamic component list based on requirements
        components = ['Client[Client Application]:::frontend']
        relationships = []
        
        # Add API Gateway if multiple services needed
        if sum(1 for req in reqs.values() if req) > 2:
            components.append('Gateway[API Gateway]:::backend')
            relationships.append('Client --> Gateway')
            last_component = 'Gateway'
        else:
            last_component = 'Client'

        # Add components based on requirements
        if reqs['needs_auth']:
            components.append('Auth[Auth Service]:::backend')
            relationships.append(f'{last_component} --> Auth')
            
        if reqs['needs_storage']:
            components.extend([
                'Storage[Storage Service]:::backend',
                'ObjectStore[(Object Store)]:::database'
            ])
            relationships.extend([
                f'{last_component} --> Storage',
                'Storage --> ObjectStore'
            ])
            
        if reqs['needs_search']:
            components.extend([
                'Search[Search Service]:::backend',
                'SearchDB[(Search Index)]:::database'
            ])
            relationships.extend([
                f'{last_component} --> Search',
                'Search --> SearchDB'
            ])

        # Build Mermaid diagram
        mermaid = f"""graph TD
    classDef frontend fill:#bbf,stroke:#333,stroke-width:2px
    classDef backend fill:#f9f,stroke:#333,stroke-width:2px
    classDef database fill:#bfb,stroke:#333,stroke-width:2px
    
    {chr(10) + '    '.join(components)}
    {chr(10) + '    '.join(relationships)}"""

        # Generate detailed response
        response = f"""# Architecture Design: {task}

```mermaid
{mermaid}
```

## Technology Stack

1. Frontend:
{chr(10).join([f'   - {t.title()}' for t in tech['frontend']]) if tech['frontend'] else '   - React.js (recommended)'}

2. Backend:
{chr(10).join([f'   - {t.title()}' for t in tech['backend']]) if tech['backend'] else '   - FastAPI (recommended)'}

3. Data Storage:
{chr(10).join([f'   - {t.title()}' for t in tech['database']]) if tech['database'] else '   - PostgreSQL (recommended)'}

## Key Components

{chr(10).join([f'- {component.split("[")[1].split("]")[0]}: Handles {self._get_component_description(component)}' for component in components])}

## Design Considerations

1. Scalability:
   - Horizontal scaling for stateless services
   - Cache layers for frequently accessed data
   - Load balancing across service instances

2. Security:
   {'- Implement OAuth2 with JWT tokens' if reqs['needs_auth'] else '- Basic authentication and authorization'}
   {'- Rate limiting and request validation' if reqs['needs_api'] else ''}
   {'- Encrypted data storage' if reqs['needs_storage'] else ''}

3. Performance:
   {'- Search optimization with indexing' if reqs['needs_search'] else ''}
   {'- Caching strategy for frequent queries' if reqs['needs_api'] else ''}
   {'- Efficient file handling and streaming' if reqs['needs_storage'] else ''}
"""
        return response

    def _get_component_description(self, component: str) -> str:
        """Generate description for architecture components."""
        component_lower = component.lower()
        if 'client' in component_lower:
            return "user interface and interaction"
        elif 'gateway' in component_lower:
            return "request routing and load balancing"
        elif 'auth' in component_lower:
            return "authentication and authorization"
        elif 'storage' in component_lower:
            return "document and file management"
        elif 'search' in component_lower:
            return "content indexing and search functionality"
        return "core business logic"