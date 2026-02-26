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

## Workshop Exercises

**[See WORKSHOP.md for the full hands-on guide.](WORKSHOP.md)**

The exercises walk you through:
1. Exploring the codebase with subagents
2. Using the pre-built code-reviewer agent
3. Building a `/check-ui` skill from scratch — make API changes and verify them
4. Seeing auto-formatting hooks in action
5. Building your own agents and skills

Start Claude Code in this directory:

```bash
claude
```

Claude reads CLAUDE.md and understands the project. The `.claude/skills/` directory is intentionally empty — building skills is the exercise.

## License

MIT
