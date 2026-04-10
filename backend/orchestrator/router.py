from memory.short_term import get_short_memory, add_to_short_memory
from memory.long_term import retrieve_long_memory
from memory.memory_manager import process_memory, filter_relevant
from llm.prompt_builder import build_prompt
from llm.llm_client import call_llm
from db.sqlite_db import save_entry
from memory.sentiment import get_sentiment

def generate_suggestion_llm(message, sentiment, memories):

    prompt = f"""
    You are a journaling assistant.

    User message: "{message}"
    Sentiment: {sentiment}

    Based on this, generate ONE short reflective journaling prompt.
    Keep it:
    - empathetic
    - concise
    - not repetitive

    Example:
    "What made today challenging for you?"
    """

    suggestion = call_llm(prompt)

    return suggestion.strip()
    
def handle_user_query(user_id, message, use_memory=True):
    try:
        trace = {}

        short_memory = get_short_memory(user_id)

        if use_memory:
            try:
                raw_memories = retrieve_long_memory(message)
                relevant_memories = filter_relevant(raw_memories) if raw_memories else []
            except:
                relevant_memories = []

            long_memory = [m["text"] for m in relevant_memories]

            trace["memory_used"] = True
            trace["memory_count"] = len(relevant_memories)

        else:
            long_memory = ""
            relevant_memories = []
            trace["memory_used"] = False
            trace["memory_count"] = 0

        # intent
        if "summarize" in message.lower():
            trace["intent"] = "reflection"
        elif "feel" in message.lower():
            trace["intent"] = "emotional_journal"
        else:
            trace["intent"] = "general_chat"

        prompt = build_prompt(message, short_memory, long_memory)
        response = call_llm(prompt)

        # sentiment
        try:
            sentiment = get_sentiment(message)
        except:
            sentiment = "neutral"

        if sentiment in ["negative", "positive"]:
            suggestion = generate_suggestion_llm(message, sentiment, relevant_memories)
        else:
            suggestion = "📝 Want to reflect on your day?"
        save_entry(user_id, message, sentiment)

        add_to_short_memory(user_id, message, response)
        process_memory(message)

        trace["sentiment"] = sentiment

        return {
            "response": response,
            "suggestion": suggestion,
            "memories_used": relevant_memories,
            "trace": trace
        }

    except Exception as e:
        print("🔥 FULL ERROR:", e)

        return {
            "response": "I'm here to listen. Tell me more about your day.",
            "suggestion": "📝 Try describing how you feel today.",
            "memories_used": [],
            "trace": {"error": str(e)}
        }