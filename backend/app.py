from fastapi import FastAPI
from models.schemas import ChatRequest
from orchestrator.router import handle_user_query
from db.sqlite_db import get_entries, get_recent_entries
from db.sqlite_db import init_db, migrate_db, delete_entry,clear_all
from llm.llm_client import call_llm

init_db()
migrate_db()

app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    return handle_user_query(
        request.user_id,
        request.message,
        request.use_memory
    )

@app.get("/entries/{user_id}")
def fetch_entries(user_id: str):
    return {"entries": get_entries(user_id)}


@app.get("/insights/{user_id}")
def insights(user_id: str):
    entries = get_entries(user_id)

    sentiment_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }

    for e in entries:
        sentiment = e.get("sentiment")

        if sentiment in sentiment_count:
            sentiment_count[sentiment] += 1

    return sentiment_count

@app.get("/weekly-reflection/{user_id}")
def weekly_reflection(user_id: str):
    entries = get_recent_entries(user_id)

    if not entries:
        return {"reflection": "No entries yet."}

    combined = "\n".join(entries)

    prompt = f"""
You are a thoughtful journal assistant.

Analyze the user's past entries and:
- Summarize their week
- Identify emotional patterns
- Give 1-2 gentle suggestions

Entries:
{combined}
"""

    reflection = call_llm(prompt)

    return {"reflection": reflection}


@app.get("/patterns/{user_id}")
def detect_patterns(user_id: str):
    entries = get_entries(user_id)

    total = len(entries)
    if total == 0:
        return {"patterns": ["No data yet"]}

    pos = sum(1 for e in entries if e["sentiment"] == "positive")
    neg = sum(1 for e in entries if e["sentiment"] == "negative")

    patterns = []

    if neg > pos:
        patterns.append("You’ve been feeling more stressed or low recently.")

    if pos > neg:
        patterns.append("You’ve been mostly positive lately — great progress!")

    if total > 5:
        patterns.append("You are journaling consistently. That’s a strong habit!")

    return {"patterns": patterns}

@app.delete("/delete/{entry_id}")
def delete(entry_id: int):
    delete_entry(entry_id)
    return {"status": "deleted"}

@app.delete("/clear/{user_id}")
def clear(user_id: str):
    clear_all(user_id)
    return {"status": "cleared"}