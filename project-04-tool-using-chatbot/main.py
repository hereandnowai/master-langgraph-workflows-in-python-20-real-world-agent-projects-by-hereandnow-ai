
from typing import Annotated, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os

# --- Environment and API Key Setup ---
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
google_api_key = os.getenv("GEMINI_API_KEY")

if not tavily_api_key or not google_api_key:
    raise ValueError("TAVILY_API_KEY and GEMINI_API_KEY must be set in your .env file")

# --- State Definition ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Tool Definition ---
# Add a detailed description to the tool to help the AI understand its purpose.
search_tool = TavilySearch(
    max_results=2,
    name="web_search",
    description="A tool that can search the internet for up-to-date information, including weather, news, and general knowledge questions."
)
tools = [search_tool]
tool_node = ToolNode(tools)

# --- Agent Definition ---
# 1. Make the system prompt more direct.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. To answer questions, you must use the 'web_search' tool. This tool is for searching the internet for real-time information like weather, news, or any other facts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# 2. Define the LLM with tools bound
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key)
llm_with_tools = llm.bind_tools(tools)

# 3. Define the agent node that uses the prompt and LLM
def agent_node(state: State):
    chain = prompt | llm_with_tools
    response = chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

# --- Graph Definition ---
def should_continue(state: State) -> Literal["tools", "__end__"]:
    """Determines the next step based on whether the last message contains tool calls."""
    if state["messages"][-1].tool_calls:
        return "tools"
    return "__end__"

# Create the graph
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()

# --- Main Interaction Loop ---
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        response = app.invoke({"messages": [("human", user_input)]})
        print(f"AI: {response['messages'][-1].content}")
