# Optional Skills

Official skills maintained by Pixel Agents that are **not activated by default**.

These skills ship with the pixel-agents repository but are not copied to
`~/.pixel-agents/skills/` during setup. They are discoverable via the Skills Hub:

```bash
pixel-agents skills browse               # browse all skills, official shown first
pixel-agents skills browse --source official  # browse only official optional skills
pixel-agents skills search <query>       # finds optional skills labeled "official"
pixel-agents skills install <identifier> # copies to ~/.pixel-agents/skills/ and activates
```

## Why optional?

Some skills are useful but not broadly needed by every user:

- **Niche integrations** — specific paid services, specialized tools
- **Experimental features** — promising but not yet proven
- **Heavyweight dependencies** — require significant setup (API keys, installs)

By keeping them optional, we keep the default skill set lean while still
providing curated, tested, official skills for users who want them.
