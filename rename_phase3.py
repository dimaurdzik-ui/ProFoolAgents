import os
import re

replacements = [
    # Longest / specific first
    ("portal.pixelagents.com", "portal.pixelagents.com"),
    ("api.pixelagents.com", "api.pixelagents.com"),
    ("pixel.api_server.capabilities", "pixel.api_server.capabilities"),
    ("pixel.tool.progress", "pixel.tool.progress"),
    ("platform: pixel-agents", "platform: pixel-agents"),
    
    # Exact case-sensitive replacements
    ("Pixel Agents", "Pixel Agents"),
    ("Pixel-Agents", "Pixel-Agents"),
    ("pixel-agents", "pixel-agents"),
    ("PIXEL-AGENTS", "PIXEL-AGENTS"),
    
    ("Pixel Agents", "Pixel Agents"),
    ("pixel-agents", "pixel-agents"),
    ("pixelagents", "pixelagents"),
    ("PIXEL_AGENTS", "PIXEL_AGENTS"),
    ("PIXELAGENTS", "PIXELAGENTS"),
    
    # Variable/Environment boundaries
    ("PIXEL_AGENTS_HOME", "PIXEL_AGENTS_HOME"),
    ("PIXEL_AGENTS_CRON", "PIXEL_AGENTS_CRON"),
    ("PIXEL_AGENTS_DESKTOP", "PIXEL_AGENTS_DESKTOP"),
    ("PIXEL_AGENTS_", "PIXEL_AGENTS_"),
    ("_PIXEL_AGENTS", "_PIXEL_AGENTS"),
    ("pixel_", "pixel_"),
    ("_pixel", "_pixel"),
    
    ("PIXEL_", "PIXEL_"),
    ("_PIXEL", "_PIXEL"),
    ("pixel_", "pixel_"),
    ("_pixel", "_pixel"),
    
    # URLs and schemes
    ("pixelagents://", "pixelagents://"),
    
    # Capitalized / Title words
    ("Pixel Agents", "Pixel Agents"),
    ("Pixel", "Pixel"),
    
    # ALL CAPS
    ("PIXEL_AGENTS", "PIXEL_AGENTS"),
    ("PIXEL", "PIXEL"),
    
    # lowercase
    ("pixel-agents", "pixel-agents"),
    ("pixel", "pixel"),
]

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return
        
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

# Skip directories
skip_dirs = {'.git', 'node_modules', '.venv', 'dist', 'build', 'release', '.mypy_cache'}
# Skip files
skip_files = {'package-lock.json', 'uv.lock', 'yarn.lock', 'pnpm-lock.yaml', 'LICENSE', 'THIRD_PARTY_NOTICES', 'OPEN_SOURCE_LICENSES', 'pixel_agents_logo.png', 'pixel_agents_sprite.png'}
skip_exts = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.icns', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm', '.sqlite', '.db', '.tflite', '.onnx', '.pdf', '.asar'}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for file in files:
        if file in skip_files:
            continue
        ext = os.path.splitext(file)[1].lower()
        if ext in skip_exts:
            continue
        if file.startswith('LICENSE') or file.startswith('THIRD_PARTY'):
            continue
        
        process_file(os.path.join(root, file))

print("Phase 3 Replacement Complete.")
