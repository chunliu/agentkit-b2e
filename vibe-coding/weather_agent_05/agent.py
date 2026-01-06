import hashlib
from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext
from veadk import Agent

def mock_weather_query(city: str, date: str, tool_context: ToolContext) -> Dict[str, Any]:
    seed = int(hashlib.sha256(f"{city}|{date}".encode()).hexdigest(), 16)
    temperature_c = (seed % 3000) / 100 - 10
    wind_kph = (seed // 97 % 4000) / 100
    humidity = seed % 60 + 20
    conditions = ["Sunny", "Cloudy", "Rain", "Overcast", "Windy", "Snow"]
    condition = conditions[seed % len(conditions)]
    return {
        "city": city,
        "date": date,
        "temperature_c": round(temperature_c, 1),
        "wind_kph": round(wind_kph, 1),
        "humidity": humidity,
        "condition": condition,
        "source": "mock",
    }

root_agent = Agent(
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    model_name="doubao-seed-1-8-251228",
    tools=[mock_weather_query],
)
