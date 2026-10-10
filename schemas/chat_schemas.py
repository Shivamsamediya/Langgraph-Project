from pydantic import BaseModel
from typing import List

# Ye API ka request format hai
class ChatRequest(BaseModel):
    # Ye user ka sawal (query) hai
    query: str

# Ye API ka response format hai
class ChatResponse(BaseModel):
    # Ye final answer hai jo agent dega
    response: str
    # Ye intermediate steps batayega, ki agent ne kya kya kiya
    steps: List[str] = []
