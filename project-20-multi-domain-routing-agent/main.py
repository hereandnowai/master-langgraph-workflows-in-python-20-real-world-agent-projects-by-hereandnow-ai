from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd
import io
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    data: str
    context: str

# Tools and LLMs
search_tool = TavilySearchResults(max_results=3)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Dummy HR policy for context
hr_policy = "Our company offers 20 days of paid vacation per year and a comprehensive health insurance plan."
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
hr_docs = text_splitter.split_text(hr_policy)
hr_vectorstore = FAISS.from_texts(hr_docs, embeddings)
hr_retriever = hr_vectorstore.as_retriever()

# Dummy CSV for finance
dummy_csv = """Category,Amount\nFood,200\nRent,1000\nTransport,50\nEntertainment,150\n"""

# Define nodes
def route_query(state: State):
    # Simple routing based on keywords
    last_message = state["messages"][-1].content.lower()
    if "finance" in last_message or "budget" in last_message:
        return "finance_agent"
    elif "hr" in last_message or "policy" in last_message:
        return "hr_agent"
    elif "marketing" in last_message or "slogan" in last_message:
        return "marketing_agent"
    else:
        return "general_chat"

def general_chat(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [("ai", response.content)]}

def finance_agent(state: State):
    df = pd.read_csv(io.StringIO(dummy_csv))
    summary = df.groupby("Category")["Amount"].sum().to_string()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Summarize this budget data: {summary}")
    return {"messages": [("ai", response.content)]}

def hr_agent(state: State):
    query = state["messages"][-1].content
    docs = hr_retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Answer based on HR policy: {context}\nQuestion: {query}")
    return {"messages": [("ai", response.content)]}

def marketing_agent(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke("Generate a marketing slogan for a new product.")
    return {"messages": [("ai", response.content)]}

# Build graph
graph = StateGraph(State)
graph.add_node("general_chat", general_chat)
graph.add_node("finance_agent", finance_agent)
graph.add_node("hr_agent", hr_agent)
graph.add_node("marketing_agent", marketing_agent)

graph.set_entry_point("route_query")
graph.add_conditional_edges(
    "route_query",
    route_query,
    {
        "finance_agent": "finance_agent",
        "hr_agent": "hr_agent",
        "marketing_agent": "marketing_agent",
        "general_chat": "general_chat",
    },
)
graph.add_edge("finance_agent", "general_chat")
graph.add_edge("hr_agent", "general_chat")
graph.add_edge("marketing_agent", "general_chat")

graph.set_finish_point("general_chat")

# Compile and run
app = graph.compile()

# Test queries
print("\n--- Finance Query ---")
response = app.invoke({"messages": [("human", "Can you give me a summary of my budget?")]})
print(response["messages"][-1].content)

print("\n--- HR Query ---")
response = app.invoke({"messages": [("human", "What is the vacation policy?")]})
print(response["messages"][-1].content)

print("\n--- Marketing Query ---")
response = app.invoke({"messages": [("human", "I need a new marketing slogan.")]})
print(response["messages"][-1].content)

print("\n--- General Query ---")
response = app.invoke({"messages": [("human", "Tell me a joke.")]})
print(response["messages"][-1].content)
