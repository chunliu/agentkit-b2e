# agentkit-b2e

A collection of Python agent examples used to demonstrate how to use VEADK and AgentKit. 

## Repository Layout

- weather-agent-01 — Minimal FastAPI agent with OpenAI-compatible API. Uses env OPENAI_API_BASE and OPENAI_API_KEY.
- agent-veadk/weather_agent_02 — Basic VEADK Agent configured via MODEL_AGENT_API_BASE and MODEL_AGENT_API_KEY.
- agents-agentkit/weather_agent_03 — AgentKit + VEADK app exposing HTTP entrypoints. Dockerfile provided.
- agents-agentkit/weather_agent_04 — AgentKit + VEADK app using demo tools. Auto-generated Dockerfile.
- agents-agentkit/hotel_booking_agent — AgentKit + Toolbox-based toolset backed by Postgres (see tools.yaml). Dockerfile and run.sh provided.
- vibe-coding/weather_agent_05 — VEADK agent demo with a mock weather tool.

## Notes

- Model names are placeholders; set to any model available via your endpoint.
- The apps listen on port 8000 by default.
- Some Dockerfiles reference a custom base image registry; replace with your own if needed.
- .env.example files show expected variables for local runs.

