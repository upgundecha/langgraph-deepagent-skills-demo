# langgraph-deepagent-skills-demo

LangGraph Deep Agents Skills Demo

A demo project showing how to build an AI Agent using [LangGraph](https://github.com/langchain-ai/langgraph) and the [`deepagents`](https://pypi.org/project/deepagents/) library with file-system-backed skills.

## Overview

This project creates an AI Agent that can autonomously triage alerts and write postmortems by loading structured skills from Markdown files at runtime. The agent uses OpenAI GPT-4o as its model and the `deepagents` filesystem backend to discover and apply skills dynamically.

## Project Structure

```
.
├── sre_agent.py              # Main agent entrypoint
├── pyproject.toml            # Project dependencies
└── skills/
    ├── triage-alert/
    │   └── SKILL.md          # Skill: triage an alert and decide how to respond
    └── write-postmortem/
        └── SKILL.md          # Skill: write a blameless postmortem for a resolved incident
```

## Skills

| Skill | Trigger | Description |
|---|---|---|
| `triage-alert` | User wants to triage an alert | Classifies severity, blast radius, recent changes, and decides whether to page or create a ticket |
| `write-postmortem` | User wants to write a postmortem | Produces a blameless postmortem with timeline, contributing factors, and action items |

## Prerequisites

- Python 3.14+
- An OpenAI API key

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/upgundecha/langgraph-deepagent-skills-demo.git
   cd langgraph-deepagent-skills-demo
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

4. Create a `.env` file with your API key:

   ```
   OPENAI_API_KEY=your-key-here
   ```

## Usage

Run the agent with the example alert triage prompt:

```bash
uv run sre_agent.py
```

The agent will triage the following alert scenario:

> p99 latency on the checkout API jumped from 180ms to 2.4s over the last 10 minutes. Error rate is normal. A deploy to the pricing service went out 15 minutes ago.

The output includes severity, blast radius, suspected cause, and a page-or-ticket decision.

## How It Works

### Filesystem Backend

`FilesystemBackend` reads and writes skill files from disk under a configurable `root_dir`. In this project it is rooted at the repository root:

```python
backend = FilesystemBackend(
    root_dir=str(sre_dir),
    virtual_mode=True,
)
```

- **`root_dir`** — all skill paths passed to `skills=` are resolved relative to this directory.
- **`virtual_mode=True`** — the agent operates on an in-memory snapshot of the directory tree rather than the live disk. No files are written or modified at runtime.

The backend is passed to `create_deep_agent`, which uses it to back the built-in filesystem tools (`read_file`, `ls`, `glob`, `grep`, etc.) and to resolve skill files.

### Skills Loading

Skills follow the [Agent Skills specification](https://agentskills.io/specification). Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (`name` and `description`) followed by step-by-step instructions the agent follows when that skill is activated.

```
skills/
└── triage-alert/
    └── SKILL.md       ← frontmatter: name + description
                          body: structured reasoning instructions
```

Skills are loaded using **progressive disclosure** — information is revealed in three levels so startup context stays compact:

| Level | What loads | When |
|---|---|---|
| **1. Metadata** | `name` and `description` from `SKILL.md` frontmatter | Agent startup, for every configured skill |
| **2. Instructions** | Full `SKILL.md` body | When the skill is invoked |
| **3. Resources** | Supporting files under `scripts/`, `references/`, `assets/` | As needed, when the instructions reference them |

Internally, `SkillsMiddleware` handles the first two levels:

1. **Discovery** — at agent start, the middleware scans the paths in `skills=["/skills"]`, parses each `SKILL.md` frontmatter, and injects the `name` and `description` into the system prompt.
2. **Read** — when the agent decides a skill is relevant, it reads the full `SKILL.md` body via the `read_file` tool.
3. **Execute** — after reading, the agent follows the instructions and reads any supporting files only as those instructions require.

This means you can add, remove, or update skills without changing any Python code — the agent picks them up on the next run.

## Adding Skills

Add a new skill by creating a directory under `skills/` with a `SKILL.md` file. The frontmatter `name` and `description` fields are used by the agent to select the skill automatically.

```
skills/
└── my-new-skill/
    └── SKILL.md
```

`SKILL.md` frontmatter:

```yaml
---
name: my-new-skill
description: Use when the user wants to ...
---
```

## Dependencies

| Package | Purpose |
|---|---|
| `deepagents` | Core deep agent framework with filesystem backend |
| `langgraph` | Graph-based agent orchestration |
| `langchain` / `langchain-openai` | LLM integration |
| `langchain-mcp-adapters` | MCP tool adapters |
| `tavily-python` | Web search tool |
| `python-dotenv` | Environment variable loading |