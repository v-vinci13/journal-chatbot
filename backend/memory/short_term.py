memory_store= {}

def get_short_memory(user_id):
    return memory_store.get(user_id, [])

def add_to_short_memory(user_id, message,response):
    if user_id  not in memory_store:
        memory_store[user_id] =[] 

    memory_store[user_id].append((message, response))

    memory_store[user_id] = memory_store[user_id][-5:]

