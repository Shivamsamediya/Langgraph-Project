from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
from core.config import settings
from agent.state import AgentState
from agent.tools import tools

# 1. LLM Model Setup
# Ye hamara "Dimag" (Brain) hai. Hum Google Gemini 1.5 Flash use kar rahe hain.
# Make sure GEMINI_API_KEY aapke .env me valid hai.
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=settings.GEMINI_API_KEY
)

# LLM ko tools ke baare me batana zaruri hai
# bind_tools() Gemini model ko hamare tools (Calculator, Web Search) ki samajh de dega
llm_with_tools = llm.bind_tools(tools)


# 2. Agent Node (The Thinker)
def call_model(state: AgentState) -> Dict[str, Any]:
    """
    Ye function (Node) LLM ko call karta hai state messages bhej kar.
    Agent decide karega ki use tool use karna hai ya final answer dena hai.
    """
    messages = state['messages']
    
    # Model ko messages pass karo
    response = llm_with_tools.invoke(messages)
    
    # Step log message update karne ke liye
    step_msg = "Agent thought and gave a response."
    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_names = [tc['name'] for tc in response.tool_calls]
        step_msg = f"Agent decided to use tools: {', '.join(tool_names)}."
    else:
        step_msg = "Agent generated the final answer."
        
    # Naya response (AIMessage) state me append ho jayega automatically
    # kyunki humne state.py me `operator.add` use kiya tha
    return {"messages": [response], "steps": [step_msg]}


# 3. Tool Executor Node (The Doer)
def execute_tools(state: AgentState) -> Dict[str, Any]:
    """
    Ye node tab run hoti hai jab LLM ne kisi tool ko call karne ko kaha ho.
    Ye actual me tools ko chalayega aur unka output memory me dalega.
    """
    # Sabse aakhri message dekho jo agent (LLM) ne diya
    last_message = state["messages"][-1]
    
    # Tools dictionary me map kar lete hain taki naam se asani se utha sakein
    tool_map = {t.name: t for t in tools}
    
    results = []
    step_logs = []
    
    # Loop over saare tool calls jo model ne maange the
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        step_logs.append(f"Executing '{tool_name}' with arguments: {tool_args}")
        
        selected_tool = tool_map.get(tool_name)
        if selected_tool:
            # Asal me tool ko execute karo yahan pe
            tool_output = selected_tool.invoke(tool_args)
            
            # Jo result aaya usko ToolMessage object banake return karna padta hai
            # Taki LLM ko pata chale ki usne jo maanga tha uska jawaab aa gaya hai
            msg = ToolMessage(
                content=str(tool_output),
                name=tool_name,
                tool_call_id=tool_call["id"] # Pata chale ki kis tool call ka jawab hai
            )
            results.append(msg)
        else:
            # Agar koi invalid tool mang liya galti se
            msg = ToolMessage(
                content=f"Error: Tool {tool_name} not found",
                name=tool_name,
                tool_call_id=tool_call["id"]
            )
            results.append(msg)
            
    # Tools ke result messages aur steps memory me bhej do
    return {"messages": results, "steps": step_logs}


# 4. Conditional Edge Router (The Decision Maker)
def should_continue(state: AgentState) -> str:
    """
    Ye function decide karta hai ki Graph ka flow kahan jayega.
    Agar tool chali hai, toh "tools" node pe jao. Nahi toh "end" kardo.
    """
    last_message = state["messages"][-1]
    
    # Agar model ne apne aakhri jawab me tool_calls di hain
    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "tools"
    
    # Agar agent ke paas answer aa gaya hai, flow end ho jayega
    return "end"
