from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Dummy knowledge base
knowledge_base_text = "LangGraph is a library for building stateful, multi-actor applications with LLMs. It is built on top of LangChain."
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(knowledge_base_text)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()

# Define the nodes
def retrieve_context(state: State):
    query = state["messages"][-1].content
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs])
    return {"context": context}

def generate_answer(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Answer the question based on the following context:\n\n{state['context']}\n\nQuestion: {state['messages'][-1].content}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("retrieve", retrieve_context)
graph.add_node("generate", generate_answer)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.set_finish_point("generate")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"messages": [("human", "What is LangGraph?")]})
print(response["messages"][-1].content)
