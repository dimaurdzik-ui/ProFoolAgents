---
sidebar_position: 3
title: "Updating & Uninstalling"
description: "How to update Pixel Agents to the latest version or uninstall it"
---

# Updating & Uninstalling

## Updating

Update to the latest version with a single command:

```bash
pixel-agents update
```

This pulls the latest code from `main`, updates dependencies, and prompts you to configure any new options that were added since your last update.

:::tip
`pixel-agents update` automatically detects new configuration options and prompts you to add them. If you skipped that prompt, you can manually run `pixel-agents config check` to see missing options, then `pixel-agents config migrate` to interactively add them.
:::

### What happens during an update

When you run `pixel-agents update`, the following steps occur:

1. **Pre-update snapshot** — a lightweight state snapshot is saved by default (covers pairing data, cron jobs, `config.yaml`, `.env`, `auth.json`, and other state files that get modified at runtime; individual files over 1 GiB are skipped so a large sessions DB never slows the update down). Controlled by `updates.pre_update_backup` (`quick` by default, `full` for a zip of all of `PIXEL_AGENTS_HOME`, `off` to disable). Recoverable via the snapshot restore flow described under [Snapshots and rollback](../user-guide/checkpoints-and-rollback.md).
2. **Git pull** — pulls the latest code from the `main` branch and updates submodules
3. **Post-pull syntax validation + auto-rollback** — after the pull, Pixel Agents compiles the nine critical files every `pixel-agents` invocation imports at startup. If any fails to parse (e.g. an orphan merge-conflict marker, an accidentally truncated file), Pixel Agents runs `git reset --hard <pre-pull-sha>` to roll the install back so your shell stays bootable. Re-run `pixel-agents update` once the upstream fix lands.
4. **Dependency install** — runs `uv pip install -e ".[all]"` to pick up new or changed dependencies
5. **Config migration** — detects new config options added since your version and prompts you to set them
6. **Gateway auto-restart** — running gateways are refreshed after the update completes so the new code takes effect immediately. Service-managed gateways (systemd on Linux, launchd on macOS) are restarted through the service manager. Manual gateways are relaunched automatically when Pixel Agents can map the running PID back to a profile.

### Updating against a non-default branch: `--branch`

By default `pixel-agents update` tracks `origin/main`. Pass `--branch <name>` to update against a different branch — useful for QA channels, feature branches, or release-candidate testing:

```bash
pixel-agents update --branch release-candidate
pixel-agents update --check --branch experimental   # preview behindness only
```

If your local checkout is on a different branch, Pixel Agents auto-stashes any uncommitted work, switches HEAD to the target branch, and then pulls. Branches that don't exist locally are auto-tracked from `origin/<name>` (`git checkout -B <name> origin/<name>`). Branches that don't exist anywhere fail cleanly — your stashed changes are restored before exit so you're never stranded in a weird state. The `main`-only fork-upstream sync logic is automatically skipped on non-`main` branches.

### Local changes on non-interactive updates

When you run `pixel-agents update` in a terminal, Pixel Agents stashes any uncommitted source-tree changes, pulls, then **asks** whether to restore them — exactly as it always has. Nothing changes for interactive updates.

When the update runs **without a terminal** — from the desktop/chat app's "Update" button or a gateway-triggered update — there's no prompt to answer. The `updates.non_interactive_local_changes` setting decides what happens to your stashed changes:

```yaml
# ~/.pixel-agents/config.yaml
updates:
  non_interactive_local_changes: stash   # default: keep + auto-restore
  # non_interactive_local_changes: discard  # throw local source edits away
```

- `stash` (default) — auto-stash, pull, then auto-restore your changes on top of the updated code. Nothing is lost; if a restore hits conflicts they're preserved in a git stash for manual recovery.
- `discard` — auto-stash and drop the stash after the pull, so the update always lands on a clean tree. Use this only on machines where you never intend to keep local edits to the Pixel Agents source. It stash-drops (not `git reset --hard` + `git clean -fd`), so ignored paths like `node_modules`, `venv`, and build outputs are never touched.

In the desktop app this is **Settings → Advanced → In-App Update Local Changes**.

### Preview-only: `pixel-agents update --check`

Want to know if an update is available before pulling? Run `pixel-agents update --check` — it fetches and compares commits against `origin/main`. No files are modified, no gateway is restarted. Useful in scripts and cron jobs that gate on "is there an update".

### Full pre-update backup: `--backup`

For high-value profiles (production gateways, shared team installs) you can opt into a full pre-pull backup of `PIXEL_AGENTS_HOME` (config, auth, sessions, skills, pairing):

```bash
pixel-agents update --backup
```

Or make it the default for every run:

```yaml
# ~/.pixel-agents/config.yaml
updates:
  pre_update_backup: full
```

`updates.pre_update_backup` is a single knob with three modes: `quick` (default — the lightweight state snapshot described above), `full` (the quick snapshot plus a complete `PIXEL_AGENTS_HOME` zip; can add minutes on large homes), and `off` (no pre-update backup at all — `--no-backup` does the same for a single run). Legacy boolean values still work: `true` means `full`, `false` means `off`.

### Windows: another `pixel-agents.exe` is running

On Windows, `pixel-agents update` will refuse to run if it detects another `pixel-agents.exe` process holding the venv's entry-point executable open — most commonly the Pixel Agents Desktop app's spawned backend, an open `pixel-agents` REPL in another terminal, or a running gateway:

```
$ pixel-agents update
✗ Another pixel-agents.exe is running:
    PID 12345  pixel-agents.exe

  Updating now would fail to overwrite ...\venv\Scripts\pixel-agents.exe because
  Windows blocks REPLACE on a running executable.

  Close Pixel Agents Desktop, exit any open `pixel-agents` REPLs, and
  stop the gateway (`pixel-agents gateway stop`) before retrying.
  Override with `pixel-agents update --force` if you've already
  confirmed those processes will not write to the venv.
```

Close the listed processes and re-run. If you're sure the concurrent process won't interfere (rare — usually only useful when an antivirus shim is mis-attributed), pass `--force` to skip the check. In that case the updater will still retry the `.exe` rename with exponential backoff and, on stubborn locks, schedule the replacement for next reboot via `MoveFileEx(MOVEFILE_DELAY_UNTIL_REBOOT)` so the update can complete.

A second, separate guard refuses to touch the venv while any process is running from its Python interpreter (the Desktop app's backend, a gateway, a Python REPL). Those processes keep native extension files (`.pyd`) locked, and a dependency sync that dies partway on an access-denied error strands the install between versions. This guard is **not** bypassed by `--force`; if you're certain the detected holders are false positives, use the explicit `pixel-agents update --force-venv`.

Expected output looks like:

```
$ pixel-agents update
Updating Pixel Agents...
📥 Pulling latest code...
Already up to date.  (or: Updating abc1234..def5678)
📦 Updating dependencies...
✅ Dependencies updated
🔍 Checking for new config options...
✅ Config is up to date  (or: Found 2 new options — running migration...)
🔄 Restarting gateways...
✅ Gateway restarted
✅ Pixel Agents updated successfully!
```

### Recommended Post-Update Validation

`pixel-agents update` handles the main update path, but a quick validation confirms everything landed cleanly:

1. `git status --short` — if the tree is unexpectedly dirty, inspect before continuing
2. `pixel-agents doctor` — checks config, dependencies, and service health
3. `pixel-agents --version` — confirm the version bumped as expected
4. If you use the gateway: `pixel-agents gateway status`
5. If `doctor` reports npm audit issues: run `npm audit fix` in the flagged directory

:::warning Dirty working tree after update
If `git status --short` shows unexpected changes after `pixel-agents update`, stop and inspect them before continuing. This usually means local modifications were reapplied on top of the updated code, or a dependency step refreshed lockfiles.
:::

### If your terminal disconnects mid-update

`pixel-agents update` protects itself against accidental terminal loss:

- The update ignores `SIGHUP`, so closing your SSH session or terminal window no longer kills it mid-install. `pip` and `git` child processes inherit this protection, so the Python environment cannot be left half-installed by a dropped connection.
- All output is mirrored to `~/.pixel-agents/logs/update.log` while the update runs. If your terminal disappears, reconnect and inspect the log to see whether the update finished and whether the gateway restart succeeded:

```bash
tail -f ~/.pixel-agents/logs/update.log
```

- `Ctrl-C` (SIGINT) and system shutdown (SIGTERM) are still honored — those are deliberate cancellations, not accidents.

You no longer need to wrap `pixel-agents update` in `screen` or `tmux` to survive a terminal drop.

### Checking your current version

```bash
pixel-agents version
```

Compare against the latest release at the [GitHub releases page](https://github.com/PixelResearch/pixel-agents/releases).

### Updating from Messaging Platforms

You can also update directly from Telegram, Discord, Slack, WhatsApp, or Teams by sending:

```
/update
```

This pulls the latest code, updates dependencies, and restarts running gateways. The bot will briefly go offline during the restart (typically 5–15 seconds) and then resume.

### Manual Update

If you installed manually (not via the quick installer):

```bash
cd /path/to/pixel-agents
# Activate the venv you created during install (outside the source tree)
export VIRTUAL_ENV="$HOME/.pixel-agents/venvs/pixel-agents-dev"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Pull latest code
git pull origin main

# Reinstall (picks up new dependencies)
uv pip install -e ".[all]"

# Check for new config options
pixel-agents config check
pixel-agents config migrate   # Interactively add any missing options
```

### Rollback instructions

If an update introduces a problem, you can roll back to a previous version:

```bash
cd /path/to/pixel-agents

# List recent versions
git log --oneline -10

# Roll back to a specific commit
git checkout <commit-hash>
uv pip install -e ".[all]"

# Restart the gateway if running
pixel-agents gateway restart
```

To roll back to a specific release tag (substitute your previous tag — e.g. a recent release like `v2026.5.16`, or any earlier tag from `git tag --sort=-version:refname`):

```bash
git checkout vX.Y.Z
uv pip install -e ".[all]"
```

:::warning
Rolling back may cause config incompatibilities if new options were added. Run `pixel-agents config check` after rolling back and remove any unrecognized options from `config.yaml` if you encounter errors.
:::

### Note for Nix users

Nix is no longer an explicitly supported install path (best-effort only) — see [Nix Setup](./nix-setup.md). If you installed via Nix flake, updates are managed through the Nix package manager:

```bash
# Update the flake input
nix flake update pixel-agents

# Or rebuild with the latest
nix profile upgrade pixel-agents
```

Nix installations are immutable — rollback is handled by Nix's generation system:

```bash
nix profile rollback
```

See [Nix Setup](./nix-setup.md) for more details.

---

## Uninstalling

```bash
pixel-agents uninstall
```

The uninstaller gives you the option to keep your configuration files (`~/.pixel-agents/`) for a future reinstall.

### Manual Uninstall

```bash
rm -f ~/.local/bin/pixel-agents
rm -rf /path/to/pixel-agents
rm -rf ~/.pixel-agents            # Optional — keep if you plan to reinstall
```

:::info
If you installed the gateway as a system service, stop and disable it first:
```bash
pixel-agents gateway stop
# Linux: systemctl --user disable pixel-agents-gateway
# macOS: launchctl remove ai.pixel-agents.gateway
```
:::
