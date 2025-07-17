from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    log_content: str
    summary: str

# Dummy log content
dummy_log = """ERROR: Disk full. Cannot write to /var/log/app.log
INFO: User 'admin' logged in from 192.168.1.100
WARNING: High CPU usage detected on server 'web-01'
ERROR: Database connection failed. Retrying...
"""

# Define the nodes
def parse_logs(state: State):
    errors = [line for line in state["log_content"].splitlines() if "ERROR" in line]
    return {"summary": "\n".join(errors)}

def summarize_errors(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(f"Summarize the following error logs:\n\n{state['summary']}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("parse_logs", parse_logs)
graph.add_node("summarize_errors", summarize_errors)
graph.set_entry_point("parse_logs")
graph.add_edge("parse_logs", "summarize_errors")
graph.set_finish_point("summarize_errors")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"log_content": dummy_log})
print(response["messages"][-1].content)
