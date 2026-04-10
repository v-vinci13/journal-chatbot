def build_prompt(user_input, short_memory, long_memory):
    short_context = "\n".join([f"User: {m[0]} | Bot: {m[1]}" for m in short_memory])

    return f"""
You are a personal AI journal assistant.

STRICT RULES:
- Only use provided memory
- Do NOT invent past events
- If no memory exists, say naturally: "I don't have past context yet"

Relevant past memories:
{long_memory}

Recent conversation:
{short_context}

User:
{user_input}

Respond naturally.
"""