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

The `.claude/skills/` directory is intentionally empty. You're going to build your first skill — one that actually looks at the running UI and tells you what it sees.

### Step 1: Create the skill

Ask Claude to build it:

```
Create .claude/skills/check-ui/SKILL.md with:
- name: check-ui
- description: "Verify the inventory app UI by checking what's actually rendered in the browser"
- disable-model-invocation: true
- Dynamic context injection using !`./scripts/check-api.sh 2>&1` to pull
  in the API state as background data
- Instructions that tell Claude to:
  1. Read the injected API data to understand what the backend thinks the state is
  2. Use agent-browser to open the frontend (http://localhost:5173), take a
     snapshot of interactive elements, and take a screenshot
  3. Compare what the UI shows vs what the API returned — do the stats match?
     Are the right number of products in the table? Are status badges showing
     the correct colors?
  4. Save the screenshot to /tmp/check-ui.png
  5. Report: what the API says, what the UI shows, whether they match, and
     a one-line verdict
  6. Close the browser when done
```

### Step 2: Baseline check

Make sure the app is running (backend on :8000, frontend on :5173), then:

```
/check-ui
```

Claude will:
1. Inject the API data (28 products, 17/7/4 split) via the `!` preprocessor
2. Open the browser, snapshot the page, take a screenshot
3. Compare the rendered stats bar and table against the API data
4. Report that everything matches

You should see something like: "API reports 28 products. UI shows 28 rows with stats bar showing 28/17/7/4. Screenshot saved. Everything matches."

**Two things happened here:**
- The `!` backtick ran `check-api.sh` *before* Claude saw the prompt (preprocessing)
- Claude *decided* to use agent-browser to visually verify (tool use)

That's the difference: `!` commands run unconditionally. Tool calls are Claude's choice, guided by your instructions.

### Step 3: Make a change, check again

In a separate terminal, create a new out-of-stock product:

```bash
curl -s -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Workshop Badge","category":"Accessories","price":4.99,"stock":0,"sku":"WS-001"}'
```

Back in Claude:

```
/check-ui
```

Now the API data shows **29 products** and **5 out of stock**. Claude opens the browser, refreshes the page, and should confirm the UI matches — a new row appeared in the table and the stats bar updated.

### Step 4: Change a status color

Patch the product's stock to trigger a visible status change:

```bash
# Replace <ID> with the id from the POST response above
curl -s -X PATCH http://localhost:8000/api/products/<ID> \
  -H "Content-Type: application/json" \
  -d '{"stock": 5}'
```

```
/check-ui
```

The API now reports **8 low stock** and **4 out of stock**. In the browser, the "Workshop Badge" row's status badge should have flipped from red ("Out of Stock") to yellow ("Low Stock"). Claude confirms the color change is visible in the UI.

### What you just learned

| Concept | How it showed up |
|---------|-----------------|
| **Dynamic injection** (`!` backtick) | API data was injected before Claude ran — it never decided to call curl |
| **Tool use** (agent-browser) | Claude decided to open the browser, snapshot, and screenshot based on your instructions |
| **`disable-model-invocation: true`** | This skill only runs when YOU type `/check-ui` — it won't fire automatically |
| **Verification loop** | Make a change → `/check-ui` → see the result. Reusable, consistent, shareable via git |

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
