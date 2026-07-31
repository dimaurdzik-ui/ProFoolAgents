import os
import re

files_to_fix = [
    "./plugins/hermes-achievements/dashboard/dist/style.css",
    "./plugins/hermes-achievements/dashboard/dist/index.js",
    "./plugins/kanban/dashboard/dist/style.css",
    "./plugins/kanban/dashboard/dist/index.js",
    "./web/src/pages/AnalyticsPage.tsx",
    "./web/src/i18n/ja.ts",
    "./web/src/i18n/af.ts",
    "./web/src/i18n/ko.ts",
    "./web/src/i18n/pt.ts",
    "./web/src/i18n/zh-hant.ts",
    "./web/src/i18n/ru.ts",
    "./web/src/i18n/types.ts",
    "./web/src/i18n/hu.ts",
    "./web/src/i18n/fr.ts",
    "./ui-tui/src/gatewayClient.ts",
    "./web/src/i18n/zh.ts",
    "./web/src/i18n/uk.ts",
    "./web/src/i18n/en.ts",
    "./web/src/i18n/tr.ts",
    "./web/src/i18n/es.ts",
    "./web/src/i18n/it.ts",
    "./web/src/i18n/ar.ts",
    "./web/src/i18n/de.ts",
    "./web/src/i18n/ga.ts",
    "./apps/desktop/src/i18n/ja.ts",
    "./apps/desktop/src/i18n/zh-hant.ts",
    "./apps/desktop/src/i18n/types.ts",
    "./apps/desktop/src/i18n/zh.ts",
    "./apps/desktop/src/i18n/en.ts",
    "./apps/desktop/src/i18n/ar.ts",
    "./ui-tui/packages/hermes-ink/src/ink/ink.tsx",
    "./apps/desktop/src/app/command-center/index.tsx"
]

def clean_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'(?i)hermes-agent\.nousresearch\.com', 'api.pixelagents.com', content)
    content = re.sub(r'(?i)hermes achievements', 'Pixel Achievements', content)
    content = re.sub(r'(?i)hermes kanban', 'Pixel Kanban', content)
    content = re.sub(r'(?i)hermes_session_at', 'pixel_session_at', content)
    content = re.sub(r'(?i)hermes-agent', 'pixel-agents', content)
    content = re.sub(r'(?i)hermes-achievement', 'pixel-achievement', content)
    content = re.sub(r'(?i)X-Hermes-Session-Token', 'X-Pixel-Session-Token', content)
    content = re.sub(r'(?i)__HERMES_PLUGIN_SDK__', '__PIXEL_PLUGIN_SDK__', content)
    content = re.sub(r'(?i)__HERMES_PLUGINS__', '__PIXEL_PLUGINS__', content)
    content = re.sub(r'(?i)__HERMES_SESSION_TOKEN__', '__PIXEL_SESSION_TOKEN__', content)
    content = re.sub(r'(?i)\bhermes\b', 'pixel-agents', content)
    content = re.sub(r'(?i)\bHermes\b', 'Pixel Agents', content)
    content = re.sub(r'(?i)nousresearch', 'pixelagents', content)
    content = re.sub(r'(?i)NousResearch', 'PixelAgents', content)
    content = re.sub(r'(?i)\bnous\b', 'pixel', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Cleaned {filepath}")

for f in files_to_fix:
    clean_file(f)
