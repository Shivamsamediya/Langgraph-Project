from typing import Annotated, TypedDict, List
import operator
from langchain_core.messages import BaseMessage

# Ye hamara "State" hai. 
# State basically ek memory object hoti hai jo graph ke har node ke paas pass hoti hai.
# Jaise jaise workflow aage badhta hai, alag alag nodes is memory ko update karti rehti hain.

class AgentState(TypedDict):
    # 'messages' list track karti hai saari conversation (User Input, Agent Thought, Tool Output)
    # Annotated aur operator.add ka matlab hai ki jab bhi hum naya message return karenge, 
    # toh wo purani list ko overwrite nahi karega, balki usme append (add) ho jayega.
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Ye custom list hai jo intermediate steps (kya kya steps agent ne liye) track karne ke liye use hoti hai
    # Taki hum user ko transparently dikha sakein ki agent andar kya kar raha tha
    steps: Annotated[List[str], operator.add]
