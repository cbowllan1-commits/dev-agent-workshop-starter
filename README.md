# Dev Agent Workshop Starter

A product inventory tracker built with FastAPI and React — designed as a workshop starter for learning Claude Code.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/aowen14/dev-agent-workshop-starter.git
cd dev-agent-workshop-starter
./setup.sh

# Run the app
./scripts/run-dev.sh
```

Backend runs on http://localhost:8000, frontend on http://localhost:5173.

## What's Inside

- **Full-stack app**: FastAPI backend + React frontend with Tailwind CSS
- **28 seed products** across 4 categories with computed stock statuses
- **REST API** with CRUD, filtering, search, and stats
- **24 passing tests** covering all endpoints
- **Claude Code config**: pre-built agent, hooks, and an empty skills directory for you to fill

## Project Structure

```
├── src/                    # FastAPI backend
│   ├── main.py             # App + endpoints
│   ├── models.py           # Pydantic models
│   ├── database.py         # In-memory store
│   └── seed_data.py        # 28 seed products
├── tests/                  # pytest test suite
├── frontend/               # React + Vite + Tailwind
│   └── src/
│       ├── App.tsx          # Main app component
│       ├── api/client.ts    # API client
│       └── components/      # UI components
├── .claude/
│   ├── agents/             # Custom agents (code-reviewer included)
│   ├── skills/             # Your skills go here!
│   └── settings.json       # Hooks and permissions
├── scripts/                # Dev scripts
├── CLAUDE.md               # Project conventions for Claude
└── setup.sh                # One-command setup
```

## Workshop Usage

This repo is designed for the [Claude Code LA Meetup](https://lu.ma/claude-code-la). Clone it, then follow the table walkthrough exercises.

Start Claude Code in this directory:

```bash
claude
```

Claude will read CLAUDE.md and understand the project. The `.claude/skills/` directory is intentionally empty — building skills is part of the workshop.

## License

MIT
