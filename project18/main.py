

from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.tools.tavily_search import TavilySearchResults

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    research_data: str

# Define the tool
tool = TavilySearchResults(max_results=3)

# Define the nodes
def conduct_research(state: State):
    query = state["messages"][-1].content
    search_results = tool.invoke(query)
    return {"research_data": str(search_results)}

def generate_report(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(f"Generate a comprehensive report based on the following research data:\n\n{state['research_data']}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("research", conduct_research)
graph.add_node("report", generate_report)
graph.set_entry_point("research")
graph.add_edge("research", "report")
graph.set_finish_point("report")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"messages": [("human", "Latest trends in renewable energy.")]})
print(response["messages"][-1].content)

