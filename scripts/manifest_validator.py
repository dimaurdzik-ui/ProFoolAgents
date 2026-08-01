#!/usr/bin/env python3
import sys
import yaml
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Constants
REQUIRED_FIELDS = {
    "id": str,
    "name": str,
    "category": str,
    "description": str,
    "system_prompt": str,
    "prompt_version": int,
}

# The canonical list of known tools / toolsets.
# We will do a fuzzy pass based on the project's known lists.
KNOWN_TOOLS = {
    "terminal", "read_file", "write_file", "web_search",
    "grep_search", "list_dir", "view_file", "run_command", "replace_file_content",
    "multi_replace_file_content", "read_url_content", "invoke_subagent",
    "send_message", "manage_subagents", "ask_question", "ask_permission",
    "delegate_task", "memory_query", "memory_add", "github_repo_view",
    "create_artifact", "update_artifact"
}
# Alias corrections
TOOL_ALIASES = {
    "terminal_cmd": "terminal",
    "file_read": "read_file",
    "file_write": "write_file",
    "search_web": "web_search",
    "create_file": "write_file",
    "edit_file": "replace_file_content",
    "subagent_create": "invoke_subagent"
}

def validate_manifests(agents_dir: Path) -> bool:
    all_valid = True
    seen_ids = set()

    yaml_files = list(agents_dir.glob("*.yaml"))
    if not yaml_files:
        logger.warning(f"No YAML files found in {agents_dir}")
        return True

    for yaml_file in yaml_files:
        logger.debug(f"Validating {yaml_file.name}...")
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not isinstance(data, dict):
                logger.error(f"{yaml_file.name}: Root element must be a dict.")
                all_valid = False
                continue

            # Check required fields
            for field_name, field_type in REQUIRED_FIELDS.items():
                if field_name not in data:
                    logger.error(f"{yaml_file.name}: Missing required field '{field_name}'.")
                    all_valid = False
                elif not isinstance(data[field_name], field_type):
                    logger.error(f"{yaml_file.name}: Field '{field_name}' must be {field_type.__name__}, got {type(data[field_name]).__name__}.")
                    all_valid = False

            if "id" in data and isinstance(data["id"], str):
                agent_id = data["id"]
                if agent_id in seen_ids:
                    logger.error(f"{yaml_file.name}: Duplicate agent id '{agent_id}'.")
                    all_valid = False
                seen_ids.add(agent_id)

            # Check tools
            allowed_tools = data.get("allowed_tools")
            if allowed_tools is not None:
                if not isinstance(allowed_tools, list):
                    logger.error(f"{yaml_file.name}: 'allowed_tools' must be a list.")
                    all_valid = False
                else:
                    for tool in allowed_tools:
                        if tool in TOOL_ALIASES:
                            logger.error(f"{yaml_file.name}: Uses deprecated tool alias '{tool}'. Use '{TOOL_ALIASES[tool]}' instead.")
                            all_valid = False
                        # We don't strictly fail on unknown tools because there might be custom tools loaded via plugins,
                        # but we can warn.
                        elif tool not in KNOWN_TOOLS and not tool.startswith("mcp__"):
                            logger.debug(f"{yaml_file.name}: Unrecognized tool '{tool}'. (Might be a plugin or custom tool)")

        except yaml.YAMLError as e:
            logger.error(f"{yaml_file.name}: Invalid YAML syntax: {e}")
            all_valid = False
        except Exception as e:
            logger.error(f"{yaml_file.name}: Error during validation: {e}")
            all_valid = False

    return all_valid

def main():
    project_root = Path(__file__).parent.parent
    agents_dir = project_root / "config" / "agents"
    
    if not agents_dir.exists():
        logger.error(f"Directory {agents_dir} does not exist.")
        sys.exit(1)

    logger.info(f"Validating agent manifests in {agents_dir}...")
    success = validate_manifests(agents_dir)
    
    if success:
        logger.info("✅ All agent manifests are valid.")
        sys.exit(0)
    else:
        logger.error("❌ Validation failed for one or more agent manifests.")
        sys.exit(1)

if __name__ == "__main__":
    main()
