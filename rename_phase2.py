import os
import re

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return
        
    original = content
    
    # Replace explicit import references
    replacements = [
        ("import pixel_state", "import pixel_state"),
        ("from pixel_state", "from pixel_state"),
        ("import pixel_constants", "import pixel_constants"),
        ("from pixel_constants", "from pixel_constants"),
        ("import pixel_bootstrap", "import pixel_bootstrap"),
        ("from pixel_bootstrap", "from pixel_bootstrap"),
        ("import pixel_logging", "import pixel_logging"),
        ("from pixel_logging", "from pixel_logging"),
        ("import pixel_time", "import pixel_time"),
        ("from pixel_time", "from pixel_time"),
        ("import pixel_state_portability", "import pixel_state_portability"),
        ("from pixel_state_portability", "from pixel_state_portability"),
        ("import pixel_state_schema", "import pixel_state_schema"),
        ("from pixel_state_schema", "from pixel_state_schema"),
        ("import pixel_state_common", "import pixel_state_common"),
        ("from pixel_state_common", "from pixel_state_common"),
        ("import pixel_state_search", "import pixel_state_search"),
        ("from pixel_state_search", "from pixel_state_search"),
        ("import pixel_cli", "import pixel_cli"),
        ("from pixel_cli", "from pixel_cli"),
        
        ("pixel_state.", "pixel_state."),
        ("pixel_constants.", "pixel_constants."),
        ("pixel_bootstrap.", "pixel_bootstrap."),
        ("pixel_logging.", "pixel_logging."),
        ("pixel_time.", "pixel_time."),
        ("pixel_state_portability.", "pixel_state_portability."),
        ("pixel_state_schema.", "pixel_state_schema."),
        ("pixel_state_common.", "pixel_state_common."),
        ("pixel_state_search.", "pixel_state_search."),
        ("pixel_cli.", "pixel_cli."),
        
        ("get_pixel_agents_home", "get_pixel_agents_home"),
        ("set_pixel_agents_home", "set_pixel_agents_home"),
        ("reset_pixel_agents_home", "reset_pixel_agents_home"),
        ("get_process_pixel_agents_home", "get_process_pixel_agents_home"),
        ("get_default_pixel_agents_root", "get_default_pixel_agents_root"),
        ("get_pixel_agents_dir", "get_pixel_agents_dir"),
        ("iter_pixel_agents_node_dirs", "iter_pixel_agents_node_dirs"),
        ("find_pixel_agents_node_executable", "find_pixel_agents_node_executable"),
        ("pixel_agents_managed_node_tree_present", "pixel_agents_managed_node_tree_present"),
        ("heal_pixel_agents_managed_node", "heal_pixel_agents_managed_node"),
        ("display_pixel_agents_home", "display_pixel_agents_home"),
        
        ("PIXEL_AGENTS_HOME", "PIXEL_AGENTS_HOME"),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root or ".venv" in root:
        continue
    for file in files:
        if file.endswith(('.py', '.ts', '.tsx', '.json', '.md', '.sh')):
            process_file(os.path.join(root, file))

print("Import replacements complete.")
