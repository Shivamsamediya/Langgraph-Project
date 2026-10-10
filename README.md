# Beginner-Friendly LangGraph Agent Workflow 🤖

Welcome to the **LangGraph Agentic Workflow** tutorial project! 
This project is designed to teach you how to build a production-style, stateful AI agent from scratch using Python. We have added extensive Hindi/Hinglish comments in the code so you know exactly *"kya ho raha hai"*.

---

## 🌟 What are we building?
We are building a **Stateful AI Workflow System** using **LangGraph**, **LangChain**, **Google Gemini**, and **FastAPI**. 

### Important Concepts Explained:

#### 1. What is an AI Agent?
Real AI agents (like ChatGPT with web search) are not just "ask and answer" chatbots. They follow a **Reasoning Loop** (often called ReAct - Reason & Act). 
- **Reason**: They think about the user's prompt.
- **Act**: If they lack information, they decide to use **Tools** (like a Calculator or Web Search).
- **Observe**: They observe the result returned by the tool.
- **Repeat**: They think again based on the new information until they have the final answer.

#### 2. Difference Between LangChain and LangGraph
- **LangChain** is great for linear pipelines (Chain A -> Chain B -> Output). 
- **LangGraph** is built for cyclic, stateful workflows. If an agent needs to use a tool, get the result, and *go back* to the LLM to think again, you need a cycle. Chains can't do cycles easily; **Graphs** are perfect for cycles and loops!

#### 3. What is State?
In a graph, data flows from one node to another. The **State** is simply a dictionary (or memory object) that gets passed along. Every node can read from it and update it. It keeps track of the entire conversation history, intermediate tool results, and any variables you need.

#### 4. Nodes and Edges
- **Nodes**: These are the actual Python functions that do the work (e.g., calling the LLM, or executing a Python math function).
- **Edges**: These connect the nodes and define the workflow direction (e.g., Go from START to Node A).

#### 5. Conditional Routing
Sometimes the workflow direction is dynamic. Should the agent stop and give the final answer, or should it go to the "Tools" node? 
A **Conditional Edge** uses a function to check the current State and returns the name of the next Node to jump to. It's the "decision maker" of the graph.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **LangGraph & LangChain**: For graph routing, agent logic, and tools.
- **Gemini SDK (`langchain-google-genai`)**: The brain of the agent.
- **FastAPI**: To serve the agent over a robust HTTP API.
- **DuckDuckGo Search**: For web search capability (requires no extra API keys!).

---

## 🚀 Setup Instructions

Follow these steps exactly to run the project locally.

### Step 1: Create a Virtual Environment
It's always best to isolate your project dependencies. Open your terminal in the project folder:
```bash
python -m venv venv
```

### Step 2: Activate the Virtual Environment
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
1. Copy `.env.example` and rename it to `.env` (or just create a `.env` file).
2. Get your free Gemini API key from Google AI Studio.
3. Paste it inside `.env`:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run the Server
Start the FastAPI server:
```bash
python main.py
```
*(Or use `uvicorn main:app --reload`)*

The server will start at `http://127.0.0.1:8000`. 
Visit `http://127.0.0.1:8000/docs` to use the interactive Swagger UI!

---

## 📂 Project Structure ("Kya ho raha hai?")

langgraph-simple/
│
├── .env.example              # Template for API keys
├── requirements.txt          # Project dependencies
├── README.md                 # Complete tutorial, theory, and setup instructions
├── postman_collection.json   # Ready-to-import Postman collection for API testing
├── main.py                   # FastAPI application entry point
│
├── core/
│   └── config.py             # Environment variables loader
│
├── schemas/
│   └── chat_schemas.py       # Pydantic models for API request/response validation
│
├── routers/
│   └── chat.py               # API route handling the /api/chat endpoint
│
└── agent/                    # ✨ Core AI Workflow Directory
    ├── state.py              # Defines the AgentState (the memory/state dictionary)
    ├── tools.py              # Custom tools (Calculator, Web Search)
    ├── nodes.py              # Graph nodes (Model execution & Tool execution)
    └── workflow.py           # StateGraph compilation, routing, and edges

Our architecture is modular but very beginner-friendly:

- `main.py`: Entry point of the FastAPI application. Sets up the server.
- `routers/chat.py`: Defines the HTTP POST endpoint `/api/chat` which bridges the user request to our agent workflow.
- `schemas/chat_schemas.py`: Uses Pydantic to validate incoming JSON requests and format the structured response.
- `core/config.py`: Loads the `.env` variables securely.
- **`agent/`** (The Core Logic):
  - `state.py`: Defines the `AgentState` schema (the memory dictionary).
  - `tools.py`: Defines what the agent can do (Calculator Tool, Web Search Tool).
  - `nodes.py`: Defines the `call_model` node (LLM) and `execute_tools` node (Action Executor). It also has the routing logic (`should_continue`).
  - `workflow.py`: Ties everything together using LangGraph `StateGraph` and conditional edges.

---

## 🧪 Testing with Postman
We have included a `postman_collection.json` file in the root directory so you can test immediately.
1. Open Postman.
2. Click **Import** and select the `postman_collection.json` file.
3. Open the "Ask Agent" request and hit **Send**.

### Example API Request Body:
```json
{
    "query": "What is the current age of Elon Musk? Add 50 to that number."
}
```

### Example Execution Flow (Internals):
1. **START** -> `agent` node gets the query.
2. The Agent (LLM) decides it doesn't know the exact current age off the top of its head. Returns a `tool_call` for `web_search`.
3. Routing edge checks the result. Since a tool was called, it routes to the `tools` node.
4. `tools` node searches DuckDuckGo. Returns the search result to state.
5. Routing edge sends it back to the `agent` node.
6. The Agent sees the age, but knows it needs to add 50. Returns a `tool_call` for `calculate`.
7. `tools` node executes the math calculation. Returns the result.
8. Goes back to the `agent` node.
9. Agent compiles the final human-readable answer. Returns "end" because no more tools are needed.
10. Final answer is sent to the user via the API response!
