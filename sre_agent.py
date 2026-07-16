import os

from pathlib import Path
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

from dotenv import load_dotenv

# Load environment variables from .env (e.g. OPENAI_API_KEY)
load_dotenv()

# Initialise the LLM. Any LangChain-compatible model string works here.
model = init_chat_model("openai:gpt-4o")

# Resolve the repository root so that all paths passed to the backend
# and the skills list are relative to the same directory.
sre_dir = Path(__file__).parent

# FilesystemBackend gives the agent a read/write interface to local disk.
# virtual_mode=True operates on an in-memory snapshot — no files are
# written or modified at runtime.
backend = FilesystemBackend(
    root_dir=str(sre_dir),
    virtual_mode=True,
)

# Build the agent with the filesystem backend and the skills directory.
# SkillsMiddleware will scan /skills at startup, inject each skill's name
# and description into the system prompt (progressive disclosure level 1),
# and read the full SKILL.md body only when a skill is activated (level 2).
agent = create_deep_agent(
    model=model,
    name="SRE_Assistant",
    backend=backend,
    skills=["/skills"],
    system_prompt="You are an SRE assistant.",
)

# Invoke the agent with an example alert triage request.
# The agent will match the message against the triage-alert skill description
# and follow its structured reasoning steps to produce a response.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Triage this alert: p99 latency on the checkout API jumped "
                    "from 180ms to 2.4s over the last 10 minutes. "
                    "Error rate is normal. A deploy to the pricing service "
                    "went out 15 minutes ago."
                ),
            }
        ]
    }
)

# Print the final response from the agent.
print(result["messages"][-1].content)