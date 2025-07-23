from typing import Annotated, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os
import asyncio
import aioconsole

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
search_tool = TavilySearch(max_results=2, name="web_search")
tools = [search_tool]
tool_node = ToolNode(tools)

# --- Agent Definition ---
# This prompt now includes the 'agent_scratchpad' placeholder.
# This is the critical change that allows the agent to see its own tool use history.
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

# This function formats the message history into the 'agent_scratchpad' format.
def format_to_agent_scratchpad(messages: list[BaseMessage]) -> list[BaseMessage]:
    scratchpad = []
    # The scratchpad should only contain tool-related messages.
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            scratchpad.append(msg)
        elif isinstance(msg, ToolMessage):
            scratchpad.append(msg)
    return scratchpad

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: State):
    # The agent node now formats the history for the scratchpad.
    agent_scratchpad = format_to_agent_scratchpad(state["messages"])
    chain = prompt | llm_with_tools
    # The 'agent_scratchpad' variable is now correctly populated.
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

memory = InMemorySaver()
app = graph.compile(checkpointer=memory)

# --- Main Interaction Loop (Asynchronous) ---
async def main():
    while True:
        user_input = await aioconsole.ainput("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        response = await app.ainvoke(
            {"messages": [("human", user_input)]},
            config={"configurable":{"thread_id": "session1"}})
        print(f"AI: {response['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())