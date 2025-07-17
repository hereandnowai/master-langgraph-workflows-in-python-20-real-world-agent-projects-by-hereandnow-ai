
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.tools.tavily_search import TavilySearchResults

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the tool
tool = TavilySearchResults(max_results=2)

# Define the chatbot
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
graph.add_node("tool", lambda state: {"messages": [tool.invoke(state["messages"][-1].content)]})
graph.set_entry_point("chatbot")
graph.add_edge("tool", "chatbot")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"messages": [("human", "What is the weather in London?")]})
print(response["messages"][-1].content)
