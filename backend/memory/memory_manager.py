from memory.long_term import add_to_long_memory

def is_important(text):
    keywords = ["I feel", "I am", "today", "goal", "want", "stress"]
    return any(k.lower() in text.lower() for k in keywords)

def process_memory(user_input):
    if is_important(user_input):
        add_to_long_memory(user_input)

def filter_relevant(memories, threshold=1.0):
    return [m["text"] for m in memories if m["score"] < threshold]        