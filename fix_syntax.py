import os
import re

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return
        
    original = content
    
    # Fix "Pixel Agents" inside camelCase/PascalCase identifiers
    # If "Pixel Agents" is followed by a word character without space, or preceded by one
    content = re.sub(r'Pixel Agents(?=[A-Z])', 'PixelAgents', content)
    content = re.sub(r'(?<=[a-z])Pixel Agents', 'PixelAgents', content)
    content = re.sub(r'Pixel Agents(?=\w)', 'PixelAgents', content)
    content = re.sub(r'(?<=\w)Pixel Agents', 'PixelAgents', content)
    
    # Also "pixel-agents" inside camelCase/PascalCase, e.g., dataset.pixelAgentsTheme
    content = re.sub(r'pixel-agents(?=[A-Z])', 'pixelAgents', content)
    content = re.sub(r'(?<=[a-zA-Z0-9_])pixel-agents', 'PixelAgents', content) # this might be risky, but dataset.pixelAgents -> dataset.pixelAgents
    
    # specifically fix root.dataset.pixelAgentsTheme -> root.dataset.pixelAgentsTheme
    content = content.replace('dataset.pixelAgents', 'dataset.pixelAgents')
    
    # Fix import { usePixelAgentsConfig }
    content = content.replace('usePixelAgentsConfig', 'usePixelAgentsConfig')
    content = content.replace('savePixelAgentsConfig', 'savePixelAgentsConfig')
    content = content.replace('getPixelAgentsConfig', 'getPixelAgentsConfig')
    content = content.replace('PixelAgentsConfig', 'PixelAgentsConfig')
    content = content.replace('PixelAgentsActiveWork', 'PixelAgentsActiveWork')
    content = content.replace('startingPixelAgentsDesktop', 'startingPixelAgentsDesktop')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed syntax in {filepath}")

skip_dirs = {'.git', 'node_modules', '.venv', 'dist', 'build', 'release', '.mypy_cache'}
skip_exts = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.icns', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm', '.sqlite', '.db', '.tflite', '.onnx', '.pdf', '.asar'}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in skip_exts:
            continue
        process_file(os.path.join(root, file))

print("Syntax fix complete.")
