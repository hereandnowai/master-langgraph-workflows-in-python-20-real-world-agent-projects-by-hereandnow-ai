from langchain_tavily import TavilySearch
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool

load_dotenv()

# Use TavilySearch for web searches
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables. Please add it to your .env file.")
web_search = TavilySearch(max_results=3, api_key=tavily_api_key)
web_search.name = "web_search"


# --- State Definition ---
class State(TypedDict):
    """Represents the state of our chatbot, holding the list of messages."""
    messages: Annotated[list, add_messages]


# --- Environment and Model Setup ---
google_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key)
# We bind the Tavily search tool to the LLM.
llm_with_tools = llm.bind_tools([web_search])


# --- Graph Nodes (These remain the same as they operate on the standard state) ---
def chatbot(state: State):
    """Invokes the LLM to decide the next action or generate a response."""
    print("--- Calling Chatbot Node ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: State):
    """Executes tools called by the LLM."""
    print("--- Calling Tool Node ---")
    tool_calls = state["messages"][-1].tool_calls
    tool_outputs = []
    for tool_call in tool_calls:
        if tool_call['name'] == web_search.name:
            output = web_search.invoke({"query": tool_call['args']['query']})
            tool_outputs.append(
                ToolMessage(content=str(output), tool_call_id=tool_call["id"])
            )
    return {"messages": tool_outputs}


# --- Conditional Edge Logic ---
def should_continue(state: State):
    """Determines the next step in the graph."""
    print("--- Evaluating Conditional Edge ---")
    if state["messages"][-1].tool_calls:
        return "tool"
    return END

# --- Graph Construction ---
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_node("tool", tool_node)
graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot", should_continue)
graph.add_edge("tool", "chatbot")
app = graph.compile()


# --- Run the Chatbot ---
system_message = SystemMessage(
    content=(
        "You are a helpful assistant that uses the web_search tool to answer questions. "
        "When asked about the weather, you must use the web_search tool to get real-time information. "
        "After getting the search results, you must analyze the text to extract the temperature, "
        "humidity, and wind speed, and then present it clearly to the user. "
        "If multiple results are available, synthesize them to provide the most likely answer. "
        "If you cannot find the specific information after searching, inform the user."
    )
)
human_message = HumanMessage(content="What is the weather in Chennai?")
initial_messages = [system_message, human_message]

print("-- Invoking Chatbot Application ---")
final_state = app.invoke({"messages": initial_messages})
final_response = final_state["messages"][-1].content
print("\n--- Final Chatbot Response ---")
print(final_response)