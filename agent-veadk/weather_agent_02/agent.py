import os
from veadk import Agent, consts

root_agent = Agent(
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    model_name="seed-1-6-250915", # <---- change model here
    model_api_base=os.getenv("MODEL_AGENT_API_BASE") or consts.DEFAULT_MODEL_AGENT_API_BASE,
    model_api_key=os.getenv("MODEL_AGENT_API_KEY") or "",
)
