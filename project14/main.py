

from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
import pandas as pd
import io

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    csv_data: str
    summary: str

# Dummy CSV content
dummy_csv = """Category,Amount
Food,200
Rent,1000
Transport,50
Entertainment,150
"""

# Define the nodes
def parse_csv(state: State):
    df = pd.read_csv(io.StringIO(state["csv_data"]))
    summary = df.groupby("Category")["Amount"].sum().to_string()
    return {"summary": summary}

def summarize_budget(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(f"Summarize the following budget data:\n\n{state['summary']}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("parse_csv", parse_csv)
graph.add_node("summarize_budget", summarize_budget)
graph.set_entry_point("parse_csv")
graph.add_edge("parse_csv", "summarize_budget")
graph.set_finish_point("summarize_budget")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"csv_data": dummy_csv})
print(response["messages"][-1].content)

