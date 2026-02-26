# Workshop Exercises

Hands-on exercises for learning Claude Code with this inventory tracker app.

## Setup

```bash
git clone https://github.com/aowen14/dev-agent-workshop-starter.git
cd dev-agent-workshop-starter
./setup.sh
```

Start the app:

```bash
# Terminal 1: backend
uv run uvicorn src.main:app --reload --port 8000

# Terminal 2: frontend
cd frontend && pnpm dev
```

Open the frontend URL shown in your terminal (usually http://localhost:5173). You should see a product inventory table with 28 products and colored status badges.

Start Claude Code:

```bash
# Terminal 3
claude
```

---

## Exercise 1: Explore with Subagents

Ask Claude to explore the project using a subagent:

```
Use a subagent to investigate this project's structure, list all
endpoints, and summarize the API surface with request/response schemas.
```

The Explore agent (Haiku, fast, read-only) does the heavy lifting. Your main context stays clean.

Run `/cost` to see how cheap it was.

---

## Exercise 2: Use the Pre-Built Code Reviewer

The repo ships with `.claude/agents/code-reviewer.md` — a read-only agent. Try it:

```
Use the code-reviewer agent to review src/main.py
```

It can read but NOT edit. Look at the agent file to see how tools and model are configured.

---

## Exercise 3: Build a `/check-ui` Skill

The `.claude/skills/` directory is intentionally empty. You're going to build your first skill.

### Step 1: Create the helper script

```
Create a scripts/check-api.sh that:
- Calls GET /api/health and prints the result
- Calls GET /api/stats and prints the result
- Calls GET /api/products and prints the first 8 products with name, category, stock, and status
- Make it executable
```

Verify it works:

```bash
./scripts/check-api.sh
```

### Step 2: Create the skill

```
Create .claude/skills/check-ui/SKILL.md with:
- name: check-ui
- description: "Verify the inventory app UI state by checking API responses"
- disable-model-invocation: true
- Dynamic context injection: !`./scripts/check-api.sh 2>&1`
- Instructions: interpret the injected data and report health status,
  inventory counts, and a one-line verdict
```

### Step 3: Test it

```
/check-ui
```

You should see a report like: "28 products, 17 in stock, 7 low stock, 4 out of stock."

### Step 4: Make a change and verify

In a separate terminal, create a new product via curl:

```bash
curl -s -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Workshop Badge","category":"Accessories","price":4.99,"stock":0,"sku":"WS-001"}'
```

Back in your Claude session:

```
/check-ui
```

Now it should report **29 products** and **5 out of stock**. The curl call changed the data, and your skill detected it.

### Step 5: Change a status color

Patch the product's stock to trigger a status change (Out of Stock → Low Stock):

```bash
# Replace <ID> with the id from the POST response
curl -s -X PATCH http://localhost:8000/api/products/<ID> \
  -H "Content-Type: application/json" \
  -d '{"stock": 5}'
```

```
/check-ui
```

Now: 29 products, **8 low stock**, **4 out of stock**. The status flipped from red to yellow.

**What you just learned**: Skills with `!` backtick syntax inject live data before Claude sees the prompt. The skill is a reusable verification step — make a change, run `/check-ui`, see the result.

---

## Exercise 4: See Hooks in Action

The repo has a PostToolUse hook in `.claude/settings.json` that auto-formats Python with ruff. Test it:

```
Add a GET /api/products/expensive endpoint that returns products
with price > 100. Write it with messy formatting.
```

Watch the output — ruff formats the file automatically after Claude writes it.

---

## Exercise 5: Build Something of Your Own

Ideas:

- **A `/test-and-commit` skill** — runs pytest, commits only if all tests pass
- **A `test-writer` agent** — reads code, writes missing tests, runs them
- **A `/project-status` skill** — injects `git log`, test count, and API stats into a dashboard

---

## Key Concepts

| Concept | What it does | Example in this repo |
|---------|-------------|---------------------|
| **CLAUDE.md** | Project conventions Claude follows automatically | Build commands, API reference, status rules |
| **Agents** | Specialized subagents with limited tools | `.claude/agents/code-reviewer.md` (read-only) |
| **Skills** | Reusable commands you invoke with `/name` | `/check-ui` (you built this) |
| **Dynamic injection** | `!`command`` runs before Claude sees the prompt | `!`./scripts/check-api.sh`` in your skill |
| **Hooks** | Shell commands that run on tool events | Auto-format Python on every edit |
