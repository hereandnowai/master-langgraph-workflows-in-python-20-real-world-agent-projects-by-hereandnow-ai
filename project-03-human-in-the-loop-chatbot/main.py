
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the chatbot
def chatbot(state: State):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Create the graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.set_finish_point("chatbot")

# Compile and run the graph with memory
memory = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}
app.invoke({"messages": [("human", "My name is John.")]}, config=config)
response = app.invoke({"messages": [("human", "What is my name?")]}, config=config)
print(response["messages"][-1].content)
