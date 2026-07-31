# Pixel Agents CLI Reference

Live sources when anything looks stale: `pixel-agents --help`, `pixel-agents <command> --help`,
https://api.pixelagents.com/docs/reference/cli-commands

### Global Flags

```
pixel-agents [flags] [command]        (no subcommand = interactive chat)

  --version, -V             Show version
  -z, --oneshot PROMPT      One-shot: print ONLY the final response (for scripts/pipes)
  -m MODEL  --provider P    Model/provider override for this invocation
  -t, --toolsets LIST       Comma-separated toolsets for this invocation
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --tui / --cli             Force the Ink TUI / classic REPL
  --ignore-rules            Skip AGENTS.md/SOUL.md/memory/skill injection
  --safe-mode               Disable ALL customizations (troubleshooting)
  --pass-session-id         Include session ID in system prompt
```

### Chat

```
pixel-agents chat [flags]
  -q, --query TEXT          Single query, non-interactive
  --image PATH              Attach a local image to a single query
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --max-turns N             Cap tool-calling iterations
  --source TAG              Session source tag (default: cli)
```
(plus the global flags above)

### Configuration

```
pixel-agents setup [section]      Wizard (model|tts|terminal|gateway|tools|agent)
pixel-agents model                Interactive model/provider picker
pixel-agents fallback [add|remove|list]  Fallback provider chain
pixel-agents config [show|edit|get|set|unset|path|env-path|check|migrate]
pixel-agents login / logout       OAuth sign-in / clear stored auth
pixel-agents doctor [--fix]       Check dependencies and config
pixel-agents status [--all]       Component status
```

### Tools & Skills

```
pixel-agents tools [list|enable NAME|disable NAME]   Per-platform toolsets (curses UI with no args)

pixel-agents skills list|browse|search QUERY|inspect ID
pixel-agents skills install ID    Hub identifier OR a direct https://…/SKILL.md URL
pixel-agents skills config        Enable/disable skills per platform
pixel-agents skills check|update|uninstall|publish PATH
pixel-agents skills tap add REPO  Add a GitHub repo as a skill source
pixel-agents bundles              Skill bundles (one /<name> alias loads several skills)
```

### MCP Servers

```
pixel-agents mcp add NAME (--url or --command) | remove | list | test NAME
pixel-agents mcp catalog | install NAME     Curated catalog install
pixel-agents mcp configure NAME             Toggle tool selection
pixel-agents mcp serve                      Run Pixel Agents as an MCP server
```
Details (transport, tool discovery, catalog): `references/native-mcp.md`.

### Gateway (Messaging Platforms)

```
pixel-agents gateway run|install|start|stop|restart|status|setup
```

20+ platforms: Telegram, Discord, Slack, WhatsApp (Baileys + Business Cloud API), iMessage (Photon — `pixel-agents photon setup`), Signal, Email, SMS, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, API Server, Webhooks. Open WebUI connects via the API Server adapter. Most adapters ship under `plugins/platforms/`.
Docs: https://api.pixelagents.com/docs/user-guide/messaging/

### Sessions

```
pixel-agents sessions list|browse|rename ID TITLE|delete ID|export OUT|prune|stats
```

### Cron / Webhooks

```
pixel-agents cron list|create SCHED|edit ID|pause|resume|run ID|remove|status
    Schedules: '30m', 'every 2h', '0 9 * * *', ISO timestamp
pixel-agents webhook subscribe NAME|list|remove NAME|test NAME
```
Webhook payloads/routes: `references/webhooks.md`.

### Profiles

```
pixel-agents profile list|create NAME (--clone|--clone-all|--clone-from)|use|show|delete
pixel-agents profile rename A B | alias NAME | export NAME | import FILE
```

### Credentials & Pools

```
pixel-agents auth                 Interactive credential manager
pixel-agents auth add [PROVIDER]  Add OAuth or API-key credential (pixel, openai-codex, qwen-oauth, …)
pixel-agents auth list|remove P IDX|reset PROVIDER|status
```
Multiple credentials per provider form a pool that rotates automatically and skips exhausted keys.

### Other

```
pixel-agents desktop / gui        Native desktop app
pixel-agents dashboard            Web admin panel + embedded chat (--stop / --status)
pixel-agents proxy                OpenAI-compatible local proxy backed by an OAuth provider
pixel-agents portal               Quick setup / sign in via Pixel Portal
pixel-agents kanban <verb>        Multi-agent work-queue board
pixel-agents project              Named multi-folder workspaces
pixel-agents skin list|use|set    Switch/tweak skins (see references/themes.md)
pixel-agents pets <verb>          Pet mascots (see references/petdex.md)
pixel-agents memory setup|status|off|reset   Memory provider
pixel-agents secrets bitwarden|onepassword   External secret stores
pixel-agents moa                  Mixture-of-Agents slots
pixel-agents hooks / security / backup / import / checkpoints / console
pixel-agents logs [-f] [errors]   View agent/error logs
pixel-agents send                 One-off message through a gateway platform
pixel-agents pairing / plugins / insights / journey / computer-use
pixel-agents acp                  ACP server (IDE integration)
pixel-agents completion bash|zsh|fish
pixel-agents update / uninstall / claw migrate
```

Plugin- and provider-supplied subcommands (e.g. `pixel-agents photon setup`) only appear once their plugin is installed/active.

### Where to Find Things

| Looking for... | Location |
|---|---|
| Config options | `pixel-agents config edit` · [Configuration docs](https://api.pixelagents.com/docs/user-guide/configuration) |
| Tools / toolsets | `pixel-agents tools list` · [Tools reference](https://api.pixelagents.com/docs/reference/tools-reference) |
| Skills catalog | `pixel-agents skills browse` · [Skills catalog](https://api.pixelagents.com/docs/reference/skills-catalog) |
| Provider setup | `pixel-agents model` · [Providers guide](https://api.pixelagents.com/docs/integrations/providers) |
| Env variables | `pixel-agents config env-path` · [Env vars reference](https://api.pixelagents.com/docs/reference/environment-variables) |
| Gateway logs | `~/.pixel-agents/logs/gateway.log` (or `pixel-agents logs`) |
| Sessions | `pixel-agents sessions browse` (reads state.db) |
