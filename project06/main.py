
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    items: list[str]

# Define the nodes
def process_item(item: str):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke(f"Process this item: {item}")]}

def aggregate_results(state: State):
    return {"messages": [("ai", f"Aggregated results: {len(state['messages'])} items processed")]}

# Create the graph
graph = StateGraph(State)
graph.add_node("aggregate", aggregate_results)
graph.add_node("process", lambda state: [process_item(i) for i in state["items"]])
graph.set_entry_point("process")
graph.add_edge("process", "aggregate")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"items": ["apple", "banana", "cherry"]})
print(response["messages"][-1].content)
