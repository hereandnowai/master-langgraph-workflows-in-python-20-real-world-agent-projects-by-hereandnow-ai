

from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain.tools import Tool
import subprocess

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    command_output: str

# Define a tool to run shell commands
def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

command_tool = Tool(
    name="run_command",
    description="Run a shell command and get its output.",
    func=run_command
)

# Define the nodes
def execute_command(state: State):
    # In a real scenario, the LLM would decide which command to run
    # For this example, we hardcode a simple command
    output = command_tool.run("ls -l")
    return {"command_output": output}

def summarize_output(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(f"Summarize the following command output:\n\n{state['command_output']}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("execute", execute_command)
graph.add_node("summarize", summarize_output)
graph.set_entry_point("execute")
graph.add_edge("execute", "summarize")
graph.set_finish_point("summarize")

# Compile and run the graph
app = graph.compile()
response = app.invoke(None)
print(response["messages"][-1].content)

