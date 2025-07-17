
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    email_content: str

# Define the nodes
def parse_email(state: State):
    return {"email_content": "The customer is asking for a refund."}

def write_response(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke(f"Write a response to this email: {state['email_content']}")]}

# Create the graph
graph = StateGraph(State)
graph.add_node("parse", parse_email)
graph.add_node("write", write_response)
graph.set_entry_point("parse")
graph.add_edge("parse", "write")

# Compile and run the graph
app = graph.compile()
response = app.invoke(None)
print(response["messages"][-1].content)
