import os

def rename_all():
    # Walk bottom-up so renaming a directory doesn't break paths for its contents
    for root, dirs, files in os.walk(".", topdown=False):
        if '.git' in root or 'node_modules' in root or '.venv' in root:
            continue
            
        # Rename files
        for file in files:
            if 'hermes' in file.lower() or 'nous' in file.lower():
                old_path = os.path.join(root, file)
                new_file = file
                new_file = new_file.replace('hermes', 'pixel_agents')
                new_file = new_file.replace('Hermes', 'Pixel_Agents')
                new_file = new_file.replace('nous', 'pixel')
                new_file = new_file.replace('Nous', 'Pixel')
                # For hyphens
                new_file = new_file.replace('pixel_agents-', 'pixel-agents-')
                new_file = new_file.replace('-pixel_agents', '-pixel-agents')
                
                new_path = os.path.join(root, new_file)
                try:
                    res = os.system(f"git mv '{old_path}' '{new_path}' 2>/dev/null")
                    if res != 0:
                        os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

        # Rename directories
        for d in dirs:
            if 'hermes' in d.lower() or 'nous' in d.lower():
                old_path = os.path.join(root, d)
                new_d = d
                new_d = new_d.replace('hermes', 'pixel_agents')
                new_d = new_d.replace('Hermes', 'Pixel_Agents')
                new_d = new_d.replace('nous', 'pixel')
                new_d = new_d.replace('Nous', 'Pixel')
                # For hyphens
                new_d = new_d.replace('pixel_agents-', 'pixel-agents-')
                new_d = new_d.replace('-pixel_agents', '-pixel-agents')
                
                new_path = os.path.join(root, new_d)
                try:
                    res = os.system(f"git mv '{old_path}' '{new_path}' 2>/dev/null")
                    if res != 0:
                        os.rename(old_path, new_path)
                    print(f"Renamed dir: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

rename_all()
