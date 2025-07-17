
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the nodes
# Define the chatbot
def chatbot(state: State):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def check_threshold(state: State):
    return len(state["messages"]) > 5

# Create the graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_node("end", lambda state: state)
graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot", check_threshold, {True: "end", False: "chatbot"})

# Compile and run the graph
app = graph.compile()
response = app.invoke({"messages": [("human", "Hello!")]})
print(response["messages"][-1].content)
