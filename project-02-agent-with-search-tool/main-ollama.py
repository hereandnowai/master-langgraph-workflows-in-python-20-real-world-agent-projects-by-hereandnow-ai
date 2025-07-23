from typing import Annotated, Literal
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os
import asyncio
import aioconsole

# --- Environment and API Key Setup ---
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY must be set in your .env file")

# --- State Definition ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Tool Definition ---
search_tool = TavilySearch(max_results=2, name="web_search")
tools = [search_tool]
tool_node = ToolNode(tools)

# --- Agent Definition ---
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a powerful research assistant. Your only job is to use the 'web_search' tool to answer questions. "
            "You must not rely on your internal knowledge. You must use the tool even if you think you know the answer."
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

def format_to_agent_scratchpad(messages: list[BaseMessage]) -> list[BaseMessage]:
    scratchpad = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            scratchpad.append(msg)
        elif isinstance(msg, ToolMessage):
            scratchpad.append(msg)
    return scratchpad

# Use the modern ChatOllama class from the correct package
llm = ChatOllama(model="llama3.1:8b")
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: State):
    agent_scratchpad = format_to_agent_scratchpad(state["messages"])
    chain = prompt | llm_with_tools
    response = chain.invoke({
        "messages": state["messages"],
        "agent_scratchpad": agent_scratchpad
    })
    return {"messages": [response]}

# --- Graph Definition ---
def should_continue(state: State) -> Literal["tools", "__end__"]:
    if state["messages"][-1].tool_calls:
        return "tools"
    return "__end__"

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()

# --- Main Interaction Loop (Asynchronous) ---
async def main():
    while True:
        user_input = await aioconsole.ainput("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        response = await app.ainvoke({"messages": [("human", user_input)]})
        print(f"AI: {response['messages'][-1].content}")

if __name__ == "__main__":
    print("Starting chatbot with local Ollama model. Make sure Ollama is running.")
    asyncio.run(main())