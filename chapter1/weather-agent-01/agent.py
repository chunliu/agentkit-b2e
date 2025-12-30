# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uuid, time, logging, os
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
    session = sessions.setdefault(session_id, {"history": []})

    # Add input to memory
    session["history"].append({"role": "user", "content": req.user_input})

    # Prepare conversation history
    messages = session["history"]

    logging.info(f"[trace={trace_id}] Invoking agent for session={session_id}")
    logging.info(f"[trace={trace_id}] Input: {messages}")

    # === Call Seed model ===
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    output = response.choices[0].message.content

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
