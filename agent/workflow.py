from langgraph.graph import StateGraph, END, START
from agent.state import AgentState
from agent.nodes import call_model, execute_tools, should_continue

def create_workflow():
    """
    Yahan hum graph structure (workflow) banate hain.
    Graph ka matlab hai Nodes (functions) aur Edges (connections) ka map.
    """
    
    # 1. StateGraph object define karo hamari state schema (AgentState) ke saath
    workflow = StateGraph(AgentState)
    
    # 2. Nodes add karo graph me
    # 'agent' node wo hai jo dimag chalata hai (LLM call)
    workflow.add_node("agent", call_model)
    
    # 'tools' node wo hai jo physical action leta hai (search, math)
    workflow.add_node("tools", execute_tools)
    
    # 3. Edges (connections) define karo
    # Pura system hamesha "agent" node se START hoga
    workflow.add_edge(START, "agent")
    
    # "agent" node ke baad system kahan jaye?
    # Hum directly nahi batayenge, hum ek function (`should_continue`) ko bolenge decide karne ko.
    workflow.add_conditional_edges(
        "agent",           # Kis node se aage badhna hai?
        should_continue,   # Wo function jo decide karega kahan jana hai
        {
            # Agar `should_continue` function "tools" return karta hai, toh "tools" node pe jao
            "tools": "tools",
            # Agar "end" return karta hai, toh workflow khatam karo (END)
            "end": END
        }
    )
    
    # Jab "tools" node apna kaam pura kar le, toh wapas "agent" node par bhejo
    # Taki agent tool ke output ko padh ke naya decision le sake
    workflow.add_edge("tools", "agent")
    
    # 4. Graph ko compile karo (Ek aisi application banao jo chal sake)
    app = workflow.compile()
    
    return app

# Hum is app object ko instantiate karke export kar rahe hain
# Ye application humari FastAPI router me use hogi
agent_app = create_workflow()
