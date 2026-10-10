from fastapi import APIRouter, HTTPException
from schemas.chat_schemas import ChatRequest, ChatResponse
from agent.workflow import agent_app
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Ye hamara main endpoint hai. Jab user POST request karega toh ye run hoga.
    """
    try:
        # 1. User ke text ko LangChain ke 'HumanMessage' object me convert karo
        user_msg = HumanMessage(content=request.query)
        
        # 2. Initial State create karo. Graph execution yahan se shuru hogi
        initial_state = {
            "messages": [user_msg],
            "steps": ["Received user query via API."]
        }
        
        # 3. LangGraph Agent ko run (invoke) karo
        # Ye graph ke through tab tak loop karega jab tak wo END tak nahi pahunch jata
        final_state = agent_app.invoke(initial_state)
        
        # 4. Final state se answer nikalna
        # Final answer hamesha messages list ke aakhri me hoga
        final_message = final_state["messages"][-1].content
        
        # Steps nikalo jo humne custom list me save kiye the
        steps_taken = final_state.get("steps", [])
        
        return ChatResponse(
            response=final_message,
            steps=steps_taken
        )
        
    except Exception as e:
        print(f"Workflow execution failed: {e}")
        # Agar koi error aaye toh user ko 500 error dikhao
        raise HTTPException(status_code=500, detail=str(e))
