import os

aliases = """
# Compatibility Aliases for Python Backend
get_pixel_agents_home_override = get_pixel_agents_home_override
set_pixel_agents_home_override = set_pixel_agents_home_override
reset_pixel_agents_home_override = reset_pixel_agents_home_override
get_pixel_agents_home = get_pixel_agents_home
get_process_pixel_agents_home = get_process_pixel_agents_home
get_default_pixel_agents_root = get_default_pixel_agents_root
get_pixel_agents_dir = get_pixel_agents_dir
iter_pixel_agents_node_dirs = iter_pixel_agents_node_dirs
find_pixel_agents_node_executable = find_pixel_agents_node_executable
pixel_agents_managed_node_tree_present = pixel_agents_managed_node_tree_present
heal_pixel_agents_managed_node = heal_pixel_agents_managed_node
display_pixel_agents_home = display_pixel_agents_home
"""

with open("pixel_constants.py", "a", encoding="utf-8") as f:
    f.write(aliases)
print("Aliases added.")
