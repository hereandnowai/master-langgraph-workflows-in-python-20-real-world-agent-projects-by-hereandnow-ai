
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
    email_content: str

# Define the nodes
def parse_email(state: State):
    return {"email_content": "The customer is asking for a refund."}

def write_response(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Write a response to this email: {state['email_content']}")
    return {"messages": [response]}

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
