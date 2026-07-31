

def test_tui_finds_bundled_entry_js(tmp_path):
    """_find_bundled_tui finds entry.js bundled in the package."""
    tui_dist = tmp_path / "pixel_cli" / "tui_dist"
    tui_dist.mkdir(parents=True)
    entry = tui_dist / "entry.js"
    entry.write_text("// bundled TUI", encoding="utf-8")

    from pixel_cli.main import _find_bundled_tui
    result = _find_bundled_tui(pixel_cli_dir=tmp_path / "pixel_cli")
    assert result is not None
    assert result.name == "entry.js"


