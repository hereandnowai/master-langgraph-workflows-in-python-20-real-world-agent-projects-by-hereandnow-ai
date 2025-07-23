# install the correct search library
# pip uninstall duckduckgo-search
# pip install ddgs

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
assert google_api_key, "Set GEMINI_API_KEY in .env or shell"

class State(TypedDict):
    question: str
    duck_snippet: str
    draft: str
    approved: bool

graph = StateGraph(State)
search_tool = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search web using DuckDuckGo and return snippet."""
    return search_tool.invoke(query)

@tool
def human_review(draft: str) -> bool:
    """Interrupt and ask for human approval of the draft."""
    res = interrupt({"draft": draft})
    return res["data"].strip().lower() in ("yes", "y", "approve")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0,
)

def do_search(state: State) -> State:
    return {"duck_snippet": web_search.invoke(state["question"])}

def draft_answer(state: State) -> State:
    prompt = (
        f"Question: {state['question']}\n\n"
        f"Found info: {state['duck_snippet']}\n\n"
        "Write a factual draft answer based on the above snippet."
    )
    resp = llm.invoke(prompt)
    text = resp.content if hasattr(resp, "content") else resp
    return {"draft": text}

def approve_node(state: State) -> State:
    return {"approved": human_review.invoke(state["draft"])}

def finalize(state: State) -> State:
    return {"draft": state["draft"] if state["approved"] else "I'll refine and resend shortly."}

graph.add_node("search", do_search)
graph.add_node("draft", draft_answer)
graph.add_node("approve", approve_node)
graph.add_node("final", finalize)
graph.add_edge(START, "search")
graph.add_edge("search", "draft")
graph.add_edge("draft", "approve")
graph.add_edge("approve", "final")
graph.add_edge("final", END)

compiled = graph.compile(checkpointer=MemorySaver())

def run_session(question: str, thread: str = "session1"):
    state = {"question": question, "duck_snippet": "", "draft": "", "approved": False}
    config = {"configurable": {"thread_id": thread}}
    stream = compiled.stream(state, config, stream_mode="values")
    for ev in stream:
        if ev.get("interrupt"):
            print("\n🤖 Draft:\n", ev["interrupt"]["data"]["draft"])
            ans = input("Approve? (yes/no): ")
            cmd = Command(resume={"data": ans})
            # ✅ Use proper config here:
            stream = compiled.stream(cmd, config, stream_mode="values")
        elif ev.get("values"):
            print("\n🎉 Final answer:", ev["values"]["draft"])

if __name__ == "__main__":
    try:
        import ddgs  # to ensure the correct library is installed
    except ImportError:
        print("🔧 Error: please install `ddgs` (pip install ddgs)")
        exit(1)

    q = input("Ask your question: ")
    run_session(q)