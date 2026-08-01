import os
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from pixel_constants import get_pixel_agents_home

class AgentTemplate:
    def __init__(self, template_id: str, name: str, description: str, system_prompt: str, tools: List[str] = None, max_task_duration_minutes: int = 30):
        self.id = template_id
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.max_task_duration_minutes = max_task_duration_minutes
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "tools": self.tools,
            "max_task_duration_minutes": self.max_task_duration_minutes
        }

def load_catalog(skills_dir: Optional[Path] = None) -> List[AgentTemplate]:
    if not skills_dir:
        # Fallback to default
        skills_dir = Path(__file__).parent.parent / "skills" / "workers"
        
    if not skills_dir.exists():
        return []

    templates = []
    for file_path in skills_dir.glob("*.md"):
        template = _parse_template(file_path)
        if template:
            templates.append(template)
            
    return templates

def get_template(template_id: str, skills_dir: Optional[Path] = None) -> Optional[AgentTemplate]:
    if not skills_dir:
        skills_dir = Path(__file__).parent.parent / "skills" / "workers"
        
    file_path = skills_dir / f"{template_id}.md"
    if not file_path.exists():
        return None
        
    return _parse_template(file_path)

def _parse_template(file_path: Path) -> Optional[AgentTemplate]:
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                body = parts[2].strip()
                
                try:
                    metadata = yaml.safe_load(frontmatter_str) or {}
                except Exception:
                    metadata = {}
                    
                # Extract fields
                template_id = metadata.get("id", file_path.stem)
                name = metadata.get("name", template_id.title().replace("-", " "))
                description = metadata.get("description", "")
                tools = metadata.get("tools", [])
                max_duration = metadata.get("max_task_duration_minutes", 30)
                
                return AgentTemplate(template_id, name, description, body, tools, max_duration)
    except Exception as e:
        print(f"Error parsing worker template {file_path}: {e}")
        
    return None
