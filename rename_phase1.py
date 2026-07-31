import os
import shutil

rename_map = {
    # Core python files
    "pixel_state.py": "pixel_state.py",
    "pixel_constants.py": "pixel_constants.py",
    "pixel_bootstrap.py": "pixel_bootstrap.py",
    "pixel_logging.py": "pixel_logging.py",
    "pixel_time.py": "pixel_time.py",
    "pixel_state_portability.py": "pixel_state_portability.py",
    "pixel_state_schema.py": "pixel_state_schema.py",
    "pixel_state_common.py": "pixel_state_common.py",
    "pixel_state_search.py": "pixel_state_search.py",
    "pixel_cli": "pixel_cli",
    
    # Executable scripts
    "pixel-agents": "pixel-agents",
    "setup-pixel-agents.sh": "setup-pixel-agents.sh",
    
    # Tests directories and files
    "tests/pixel_cli": "tests/pixel_cli",
    "tests/pixel_state": "tests/pixel_state",
    "tests/test_pixel_state.py": "tests/test_pixel_state.py",
    "tests/test_pixel_bootstrap.py": "tests/test_pixel_bootstrap.py",
    "tests/test_pixel_logging.py": "tests/test_pixel_logging.py",
    "tests/test_pixel_state_compression_locks.py": "tests/test_pixel_state_compression_locks.py",
    "tests/test_pixel_home_profile_warning.py": "tests/test_pixel_home_profile_warning.py",
    "tests/test_pixel_constants.py": "tests/test_pixel_constants.py",
    "tests/test_pixel_state_wal_fallback.py": "tests/test_pixel_state_wal_fallback.py",
    "tests/test_pixel_state_readonly_preflight.py": "tests/test_pixel_state_readonly_preflight.py",
    
    # Electron/React specific
    "apps/desktop/src/types/pixel-agents.ts": "apps/desktop/src/types/pixel-agents.ts",
    "apps/desktop/src/pixel-agents.ts": "apps/desktop/src/pixel-agents.ts",
    "apps/desktop/src/pixel-agents.test.ts": "apps/desktop/src/pixel-agents.test.ts",
    "apps/desktop/src/pixel-agents-parity.test.ts": "apps/desktop/src/pixel-parity.test.ts",
    "apps/desktop/src/pixel-agents-cron-scope.test.ts": "apps/desktop/src/pixel-cron-scope.test.ts",
    "apps/desktop/src/pixel-agents-profile-scope.test.ts": "apps/desktop/src/pixel-profile-scope.test.ts",
    "apps/desktop/src/app/session/hooks/use-pixel-agents-config.ts": "apps/desktop/src/app/session/hooks/use-pixel-config.ts",
    "apps/desktop/src/app/session/hooks/use-pixel-agents-config.test.ts": "apps/desktop/src/app/session/hooks/use-pixel-config.test.ts",
    "apps/desktop/electron/windows-pixel-agents-path.ts": "apps/desktop/electron/windows-pixel-path.ts",
    "apps/desktop/electron/windows-pixel-agents-path.test.ts": "apps/desktop/electron/windows-pixel-path.test.ts",
}

for old, new in rename_map.items():
    if os.path.exists(old):
        # Using git mv if it's tracked, otherwise regular mv
        res = os.system(f"git mv '{old}' '{new}' 2>/dev/null")
        if res != 0:
            os.rename(old, new)
        print(f"Renamed {old} -> {new}")
    else:
        print(f"Not found: {old}")
