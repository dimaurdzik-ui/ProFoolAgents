import os
import json

# Replace pyproject.toml
try:
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('name = "pixel-agents"', 'name = "pixel-agents"')
    content = content.replace('authors = [{ name = "Pixel Agents" }]', 'authors = [{ name = "Pixel Agents" }]')
    content = content.replace('pixel-agents=pixel_cli.main:main', 'pixel-agents=pixel_cli.main:main')
    content = content.replace('pixel-agents = "pixel_cli.main:main"', 'pixel-agents = "pixel_cli.main:main"')
    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(content)
except Exception as e:
    print(f"Error pyproject.toml: {e}")

# Replace package.json in desktop app
try:
    with open('apps/desktop/package.json', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('"name": "pixel-agents-desktop"', '"name": "pixel-agents-desktop"')
    content = content.replace('"author": "Pixel Agents"', '"author": "Pixel Agents"')
    content = content.replace('com.pixelagents.pixel-agents', 'com.pixelagents.desktop')
    content = content.replace('pixelagents://', 'pixelagents://')
    content = content.replace('pixel-agents.png', 'pixel_agents_logo.png')
    content = content.replace('pixel-agents-sprite.png', 'pixel_agents_sprite.png')
    content = content.replace('Pixel Agents Desktop', 'Pixel Agents Desktop')
    content = content.replace('Pixel Agents', 'Pixel Agents')
    with open('apps/desktop/package.json', 'w', encoding='utf-8') as f:
        f.write(content)
except Exception as e:
    print(f"Error package.json: {e}")

# Strip all pixel-agents dependencies
try:
    with open('apps/desktop/package.json', 'r', encoding='utf-8') as f:
        pkg = json.loads(f.read())
    if 'dependencies' in pkg:
        keys_to_remove = [k for k in pkg['dependencies'] if 'pixel-agents' in k or 'pixelagents' in k]
        for k in keys_to_remove:
            del pkg['dependencies'][k]
    with open('apps/desktop/package.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(pkg, indent=2))
except Exception as e:
    print(f"Error strip deps: {e}")

print("Metadata updated.")
