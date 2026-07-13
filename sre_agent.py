import os

from pathlib import Path
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model("openai:gpt-4o")

sre_dir = Path(__file__).parent
    
backend = FilesystemBackend(
    root_dir=str(sre_dir),
    virtual_mode=True,
)

agent = create_deep_agent(
    model=model,
    name="SRE_Assistant",
    backend=backend,
    skills=["/skills"],
    system_prompt="You are an SRE assistant.",
)

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

print(result["messages"][-1].content)