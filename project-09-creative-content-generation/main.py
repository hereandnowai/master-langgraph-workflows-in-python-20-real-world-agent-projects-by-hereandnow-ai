
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the nodes
def generate_slogan(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke("Generate a marketing slogan for a new coffee shop.")
    return {"messages": [response]}

def refine_slogan(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Refine this slogan: {state['messages'][-1].content}")
    return {"messages": [response]}

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
