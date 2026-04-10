from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str
    use_memory: bool = True 
    