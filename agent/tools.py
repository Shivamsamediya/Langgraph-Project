from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Calculator Tool
# @tool decorator kisi bhi normal python function ko LangChain tool bana deta hai.
# LLM is function ka docstring (description) padh ke samajh jata hai ki ise kab use karna hai.
@tool
def calculate(expression: str) -> str:
    """Useful for mathematical calculations. Provide a valid mathematical expression in python (e.g. 50 * 5)."""
    try:
        # eval() math expression ko execute karta hai string se
        # Note: Production me complex ya secure system me eval() ki jagah proper math parser use karein
        result = str(eval(expression))
        return f"Result is {result}"
    except Exception as e:
        return f"Error calculating: {e}"

# 2. Web Search Tool
# Ye directly DuckDuckGo search API use karega bina kisi extra API key ke.
# Bahut useful hai current events, facts ya fresh information nikalne ke liye.
web_search_tool = DuckDuckGoSearchRun(
    name="web_search",
    description="Useful for searching the internet for current events, news, or general facts. Provide a query string."
)

# Hum ek list bana lete hain taki agent setup me pass kar sakein
tools = [calculate, web_search_tool]
