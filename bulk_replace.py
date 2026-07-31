import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files
        
    if "pixel-agents" not in content.lower() and "pixel" not in content.lower():
        return
        
    content = content.replace("pixel-agents", "pixel-agents")
    content = content.replace("pixel-agents", "pixel-agents")
    content = content.replace("Pixel Agents", "Pixel Agents")
    content = content.replace("PIXEL_AGENTS", "PIXEL_AGENTS")
    content = content.replace("pixel-agents", "pixel-agents")
    content = content.replace("pixel", "pixel")
    content = content.replace("Pixel", "Pixel")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk("apps/desktop/src"):
    for file in files:
        if file.endswith(('.ts', '.tsx', '.json', '.css', '.html')):
            replace_in_file(os.path.join(root, file))

for root, dirs, files in os.walk("apps/desktop/electron"):
    for file in files:
        if file.endswith(('.ts', '.tsx', '.json', '.js')):
            replace_in_file(os.path.join(root, file))

print("Bulk replacement complete.")
