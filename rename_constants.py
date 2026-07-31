import os
import re

file_path = "pixel_constants.py"
with open(file_path, "r") as f:
    content = f.read()

# Replace strings
content = content.replace("PIXEL_AGENTS_HOME", "PIXEL_AGENTS_HOME")
content = content.replace(".pixel-agents", ".pixel-agents")
content = content.replace("pixel-agents", "pixel-agents")
content = content.replace('"pixel-agents"', '"pixel-agents"')
content = content.replace("'pixel-agents'", "'pixel-agents'")
content = content.replace("pixel-agents.db", "state.db") 
content = content.replace("pixel_", "pixel_agents_")
content = content.replace("PIXEL_AGENTS", "PIXEL_AGENTS")
content = content.replace("Pixel Agents", "Pixel Agents")

with open(file_path, "w") as f:
    f.write(content)

print("Updated pixel_constants.py")
