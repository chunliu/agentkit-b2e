# main.py
from unittest import result
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uuid, time, logging, os, json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# === Config model ===
MODEL_NAME = "seed-1-6-250915"
API_BASE = os.getenv("OPENAI_API_BASE")  
API_KEY = os.getenv("OPENAI_API_KEY")

# === Initialize client ===
client = OpenAI(api_key=API_KEY, base_url=API_BASE)

# === Logging setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# === Mock weather function ===
def get_weather(city: str) -> str:
    """Return current weather for a given city (mocked)."""
    fake_data = {
        "Singapore": "32°C, humid",
        "London": "12°C, cloudy",
        "Tokyo": "25°C, sunny",
    }
    return fake_data.get(city, f"Weather data unavailable for {city}")

# === Agent reasoning ===
def run_agent_reasoning(messages) -> Dict[str, Any]:
    """
    ReAct-style reasoning:
    The model decides whether to call a tool.
    Expected output JSON: {"action": "tool_name", "args": {...}} or {"action": "final_answer", "output": "..."}
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_tokens=256,
    )
    content = (response.choices[0].message.content or "").strip()

    # Try to parse JSON output
    try:
        return json.loads(content)
    except Exception:
        return {"action": "final_answer", "output": content}

# === In-memory session store ===
sessions = {}

# === FastAPI app ===
app = FastAPI(title="Weather Agent", version="0.1")

# === Request schema ===
class AgentRequest(BaseModel):
    session_id: str | None = None
    user_input: str

# === Runtime endpoint ===
@app.post("/invoke_agent")
async def invoke_agent(req: AgentRequest, request: Request):
    trace_id = str(uuid.uuid4())
    start_time = time.time()

    session_id = req.session_id or str(uuid.uuid4())
    session = sessions.setdefault(session_id, {
        "history": [
            {
                "role": "system",
                "content": (
                    "You are an intelligent agent. "
                    "You can call tools by responding with JSON in this format:\n"
                    '{"action": "<tool_name>", "args": {...}}.\n'
                    "Available tools:\n"
                    "- get_weather(city: str)\n"
                    "If you can answer directly, respond with:\n"
                    '{"action": "final_answer", "output": "..."}'
                )
            }
        ]
    })

    # Add input to memory
    session["history"].append({"role": "user", "content": req.user_input})

    reasoning = run_agent_reasoning(session["history"])
    output = ""
    if reasoning["action"] == "final_answer":
        output = reasoning.get("output", "")
    else:
        tool_name = reasoning["action"]
        tool_args = reasoning.get("args", {})
        if tool_name == "get_weather":
            output = get_weather(**tool_args)
            session["history"].append({
                "role": "system",
                "content": f"Tool {tool_name} returned: {output}"
            })
            # Prepare conversation history
            messages = session["history"]

            # === Call Seed model ===
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=512,
            )

            output = response.choices[0].message.content
        else:
            output = f"Error: Tool {tool_name} not found."

    # Store model output in memory
    session["history"].append({"role": "assistant", "content": output})

    elapsed = round(time.time() - start_time, 2)
    logging.info(f"[trace={trace_id}] Completed in {elapsed}s")

    return {
        "trace_id": trace_id,
        "session_id": session_id,
        "response": output,
        "elapsed_sec": elapsed,
    }
