
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the agents
def researcher(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke("Research the latest trends in AI.")]}

def writer(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke(f"Write a blog post about: {state['messages'][-1].content}")]}

# Create the graph
graph = StateGraph(State)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")

# Compile and run the graph
app = graph.compile()
response = app.invoke(None)
print(response["messages"][-1].content)
