import logging
from typing import Any

from veadk import Agent, Runner

from agentkit.apps import AgentkitSimpleApp
# from veadk.prompts.agent_default_prompt import DEFAULT_DESCRIPTION, DEFAULT_INSTRUCTION
from toolbox_core import ToolboxSyncClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = AgentkitSimpleApp()

agent_name = "hotel_booking_agent"
description = "A hotel booking agent designed for demo purpose." 
system_prompt = "You are a helpful hotel booking agent. You can book a hotel room for a specific date range." 

toolbox_client = ToolboxSyncClient("http://127.0.0.1:5000")
tools: list[Any] = toolbox_client.load_toolset()

agent = Agent(
    name=agent_name,
    description=description,
    instruction=system_prompt,
    tools=tools,
)
runner = Runner(agent=agent)


@app.entrypoint
async def run(payload: dict, headers: dict) -> str:
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]

    logger.info(
        f"Running agent with prompt: {prompt}, user_id: {user_id}, session_id: {session_id}"
    )
    response = await runner.run(messages=prompt, user_id=user_id, session_id=session_id)

    logger.info(f"Run response: {response}")
    return response


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
