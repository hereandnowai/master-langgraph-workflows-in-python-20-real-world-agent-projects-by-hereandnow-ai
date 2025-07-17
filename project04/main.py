
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.interrupt import TimeTravel

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the chatbot
def chatbot(state: State):
    return {"messages": [ChatGoogleGenerativeAI(model="gemini-2.5-flash").invoke(state["messages"])]}

# Create the graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_node("human", lambda state: state)
graph.set_entry_point("chatbot")
graph.add_edge("human", "chatbot")

# Compile and run the graph with a human-in-the-loop
app = graph.compile()
while True:
    response = app.invoke({"messages": [("human", input("You: "))]})
    print(f"AI: {response['messages'][-1].content}")
