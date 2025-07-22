import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")
if not KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

# --- State Definition ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Chatbot node: generates draft response ---
def chatbot(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=KEY)
    draft = llm.invoke(state["messages"])
    return {"messages": [draft]}

# --- Human review node: asks user to approve/edit ---
def human_review(state: State):
    draft = state["messages"][-1].content
    print("\n--- AI draft ---")
    print(draft)
    user_input = interrupt("Please edit or approve the above response:")
    # Return the human-approved version
    return {"messages": [{"role": "assistant", "content": user_input["data"]}]}

# --- Build the graph ---
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_node("human_review", human_review)

graph.set_entry_point("chatbot")
graph.add_edge("chatbot", "human_review")
graph.set_finish_point("human_review")

# --- Compile with in-memory memory saver ---
memory = InMemorySaver()
app = graph.compile(checkpointer=memory)

# --- Terminal Chat Loop ---
print("🤖 Human-in-the-Loop Chatbot (type 'exit' to quit)")
session_id = "cli-session"
while True:
    user = input("\nYou: ")
    if user.lower() in ("exit", "quit"):
        break

    state = {"messages": [HumanMessage(content=user)]}
    res = app.invoke(
        {"messages": state["messages"]},
        config={"configurable": {"thread_id": session_id}}
    )
    final_msg = res["messages"][-1].content
    print("Bot:", final_msg)

print("Session ended.")