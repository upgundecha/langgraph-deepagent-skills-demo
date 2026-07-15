# langgraph-deepagent-skills-demo

LangGraph Deep Agents Skills Demo

A demo project showing how to build an SRE (Site Reliability Engineering) assistant using [LangGraph](https://github.com/langchain-ai/langgraph) and the [`deepagents`](https://pypi.org/project/deepagents/) library with file-system-backed skills.

## Overview

This project creates an AI-powered SRE assistant that can autonomously triage alerts and write postmortems by loading structured skills from Markdown files at runtime. The agent uses OpenAI GPT-4o as its model and the `deepagents` filesystem backend to discover and apply skills dynamically.

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