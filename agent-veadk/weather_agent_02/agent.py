import os
from veadk import Agent, consts

def get_weather(city: str) -> str:
    """
    Get the weather for a given city.
    
    Args:
        city (str): The name of the city.
        
    Returns:
        str: The weather information for the city.
    """
    fake_data = {
        "Singapore": "32°C, humid",
        "London": "12°C, cloudy",
        "Tokyo": "25°C, sunny",
    }
    return fake_data.get(city, f"Weather data unavailable for {city}")

root_agent = Agent(
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    model_name="seed-1-6-250915", # <---- change model here
    model_api_base=os.getenv("MODEL_AGENT_API_BASE") or consts.DEFAULT_MODEL_AGENT_API_BASE,
    model_api_key=os.getenv("MODEL_AGENT_API_KEY") or "",
    model_extra_config={"extra_body": {"thinking": {"type": "disabled"}}}, # disable thinking
    tools=[get_weather],
)
