from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from dotenv import load_dotenv
import os

load_dotenv()

# DuckDuckGo tool (works with bind_tools)
web_search = DuckDuckGoSearchRun(max_results=3)

# Graph state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Model setup
google_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key)
llm_with_tools = llm.bind_tools([web_search])

def chatbot(state: State):
    print("--- Chatbot Node ---")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: State):
    print("--- Tool Node ---")
    calls = state["messages"][-1].tool_calls
    outputs = []
    for call in calls:
        if call["name"] == web_search.name:
            tool_out = web_search.invoke(call["args"]["query"])
            outputs.append(ToolMessage(content=str(tool_out), tool_call_id=call["id"]))
    return {"messages": outputs}

def should_continue(state: State):
    print("--- Conditional Edge ---")
    if state["messages"][-1].tool_calls:
        return "tool"
    return END

# Build the graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_node("tool", tool_node)
graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot", should_continue)
graph.add_edge("tool", "chatbot")
app = graph.compile()

# Run
system_message = SystemMessage(content=(
    "You are a helpful assistant that uses web_search to fetch real-time info. "
    "When asked about weather, you must call the tool, parse temperature, humidity, wind speed, "
    "and summarize clearly. If not found, say so."
))
human_message = HumanMessage(content="What is the weather in Chennai?")
initial_messages = [system_message, human_message]

print("-- Invoking Chatbot ---")
final_state = app.invoke({"messages": initial_messages})
print("\n--- Final Response ---")
print(final_state["messages"][-1].content)