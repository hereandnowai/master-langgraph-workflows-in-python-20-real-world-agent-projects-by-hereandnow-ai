

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
    candidate_response: str

# Dummy knowledge base for assessment criteria
assessment_criteria = "Key skills: Python, LangGraph, problem-solving. Look for clear explanations."
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(assessment_criteria)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()

# Define the nodes
def assess_response(state: State):
    query = state["candidate_response"]
    docs = retriever.get_relevant_documents("assessment criteria")
    context = "\n".join([d.page_content for d in docs])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
    response = llm.invoke(f"Assess the candidate response based on these criteria: {context}\nCandidate response: {query}")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("assessor", assess_response)
graph.set_entry_point("assessor")
graph.set_finish_point("assessor")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"candidate_response": "I solved the problem using a state machine in Python."})
print(response["messages"][-1].content)