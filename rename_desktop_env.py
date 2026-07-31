import os

file_path = "apps/desktop/package.json"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("PIXEL_AGENTS_DESKTOP_", "PIXEL_AGENTS_DESKTOP_")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {file_path}")
