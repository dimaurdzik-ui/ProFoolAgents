from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\pixel-agents\\pixel-agents\\venv\\Scripts" in doc
    assert "Get-Command pixel-agents        # should print C:\\Users\\<you>\\AppData\\Local\\pixel-agents\\pixel-agents\\venv\\Scripts\\pixel-agents.exe" in doc
    assert '$pixelAgentsBin = "$InstallDir\\venv\\Scripts"' in install
