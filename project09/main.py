
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the nodes
def generate_slogan(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke("Generate a marketing slogan for a new coffee shop.")]}

def refine_slogan(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke(f"Refine this slogan: {state['messages'][-1].content}")]}

# Create the graph
graph = StateGraph(State)
graph.add_node("generate", generate_slogan)
graph.add_node("refine", refine_slogan)
graph.set_entry_point("generate")
graph.add_edge("generate", "refine")
graph.add_edge("refine", "generate")

# Compile and run the graph
app = graph.compile()
response = app.invoke(None, {"recursion_limit": 3})
print(response["messages"][-1].content)
