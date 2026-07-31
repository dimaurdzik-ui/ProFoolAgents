import os
import yaml
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger("pixel_state")

@dataclass
class AgentTemplate:
    id: str
    name: str
    category: str
    description: str
    prompt_version: int
    allowed_tools: List[str]
    starter_prompts: List[str]
    capabilities: List[str]
    system_prompt: str
    enabled: bool = True
    icon: Optional[str] = None
    default_provider: Optional[str] = None
    default_model: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "prompt_version": self.prompt_version,
            "allowed_tools": self.allowed_tools,
            "starter_prompts": self.starter_prompts,
            "capabilities": self.capabilities,
            "system_prompt": self.system_prompt,
            "enabled": self.enabled,
            "icon": self.icon,
            "default_provider": self.default_provider,
            "default_model": self.default_model,
        }

class AgentRegistry:
    _instance = None
    _templates: Dict[str, AgentTemplate] = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AgentRegistry()
            cls._instance.reload()
        return cls._instance

    def reload(self):
        self._templates.clear()
        
        # Determine the root directory of the project
        project_root = Path(__file__).parent.parent
        agents_dir = project_root / "config" / "agents"
        
        if not agents_dir.exists():
            # Try to resolve relative to cwd
            agents_dir = Path(os.getcwd()) / "config" / "agents"
            
        if not agents_dir.exists():
            logger.warning(f"Agents directory {agents_dir} not found. Agent catalog will be empty.")
            return

        for yaml_file in agents_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                
                if not data or not isinstance(data, dict):
                    continue

                agent_id = str(data.get("id", ""))
                agent_name = str(data.get("name", ""))
                
                if not agent_id or not agent_name:
                    logger.warning(f"Agent template {yaml_file} is missing 'id' or 'name'. Skipping.")
                    continue
                    
                if "system_prompt" not in data or not isinstance(data["system_prompt"], str):
                    logger.warning(f"Agent template {yaml_file} is missing 'system_prompt' or has invalid type. Skipping.")
                    continue
                    
                if "category" not in data or not isinstance(data["category"], str):
                    logger.warning(f"Agent template {yaml_file} is missing 'category' or has invalid type. Skipping.")
                    continue
                    
                if "description" not in data or not isinstance(data["description"], str):
                    logger.warning(f"Agent template {yaml_file} is missing 'description' or has invalid type. Skipping.")
                    continue

                if "prompt_version" not in data or not isinstance(data["prompt_version"], int):
                    logger.warning(f"Agent template {yaml_file} is missing 'prompt_version' or has invalid type. Skipping.")
                    continue
                    
                starter_prompts = data.get("starter_prompts", [])
                if not isinstance(starter_prompts, list):
                    logger.warning(f"Agent template {yaml_file} has invalid 'starter_prompts' type. Skipping.")
                    continue
                    
                if agent_id in self._templates:
                    logger.warning(f"Agent ID '{agent_id}' from {yaml_file} is a duplicate. Skipping.")
                    continue
                    
                # Support enabled flag, defaulting to True
                enabled = data.get("enabled", True)
                if not isinstance(enabled, bool):
                    logger.warning(f"Agent template {yaml_file} has invalid 'enabled' type. Skipping.")
                    continue
                if not enabled:
                    logger.info(f"Agent template '{agent_id}' is disabled. Skipping.")
                    continue

                allowed_tools = data.get("allowed_tools")
                if allowed_tools is None:
                    allowed_tools = []
                elif not isinstance(allowed_tools, list):
                    logger.warning(f"Agent template {yaml_file} has invalid 'allowed_tools' type. Skipping.")
                    continue
                    
                capabilities = data.get("capabilities", [])
                if not isinstance(capabilities, list):
                    logger.warning(f"Agent template {yaml_file} has invalid 'capabilities' type. Skipping.")
                    continue

                template = AgentTemplate(
                    id=agent_id,
                    name=agent_name,
                    category=data["category"],
                    description=data["description"],
                    prompt_version=data["prompt_version"],
                    allowed_tools=allowed_tools,
                    starter_prompts=starter_prompts,
                    capabilities=capabilities,
                    system_prompt=data["system_prompt"],
                    enabled=True,
                    icon=data.get("icon"),
                    default_provider=data.get("default_provider"),
                    default_model=data.get("default_model")
                )
                self._templates[template.id] = template
                logger.info(f"Loaded agent template: {template.id} (v{template.prompt_version})")
            except Exception as e:
                logger.error(f"Error loading agent template from {yaml_file}: {e}")

    def get_template(self, agent_id: str) -> Optional[AgentTemplate]:
        template = self._templates.get(agent_id)
        if template is None:
            # The desktop gateway is intentionally long-lived while a developer
            # can add templates through HMR/source updates. Retry from disk once
            # before declaring an id unavailable, so a newly-added team member
            # does not require restarting the whole backend process.
            self.reload()
            template = self._templates.get(agent_id)
        return template

    def get_all_templates(self) -> List[AgentTemplate]:
        return list(self._templates.values())

def get_agent_template(agent_id: str) -> Optional[AgentTemplate]:
    return AgentRegistry.get_instance().get_template(agent_id)

def get_all_agent_templates() -> List[AgentTemplate]:
    return AgentRegistry.get_instance().get_all_templates()


TEAM_AGENT_ID = "pixel-team"


def build_team_directory(current_agent_id: str | None = None) -> str:
    """Return a compact, prompt-safe directory of available colleagues."""
    colleagues = [
        template
        for template in get_all_agent_templates()
        if template.id != TEAM_AGENT_ID and template.id != current_agent_id
    ]
    if not colleagues:
        return ""

    entries = "\n".join(
        f"- {template.name} ({template.category}): {template.description}"
        for template in colleagues
    )
    return (
        "\n\n[Команда Pixel Agents]\n"
        "Ти працюєш поруч із такими спеціалістами:\n"
        f"{entries}\n"
        "Якщо завдання виходить за межі твоєї ролі, прямо запропонуй залучити "
        "відповідного колегу. Не вигадуй результат його роботи."
    )

# Alias used by methods_agents.py
get_agent_catalog = get_all_agent_templates
