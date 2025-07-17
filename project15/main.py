
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Define the state for our graph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    resume_text: str
    job_description: str
    match_score: str

# Dummy data
dummy_resume = "Experienced software engineer with Python and machine learning skills."
dummy_job_description = "Seeking a Python developer with experience in AI and data analysis."

# Create a vector store for job descriptions (or resumes)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Define the nodes
def compare_documents(state: State):
    resume_vec = embeddings.embed_query(state["resume_text"])
    job_vec = embeddings.embed_query(state["job_description"])
    # Simple dot product for similarity (can be replaced with more complex logic)
    score = sum(a * b for a, b in zip(resume_vec, job_vec))
    return {"match_score": str(score)}

def generate_feedback(state: State):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(f"Based on a match score of {state['match_score']}, provide feedback on how well the resume matches the job description.")
    return {"messages": [("ai", response.content)]}

# Create the graph
graph = StateGraph(State)
graph.add_node("compare", compare_documents)
graph.add_node("feedback", generate_feedback)
graph.set_entry_point("compare")
graph.add_edge("compare", "feedback")
graph.set_finish_point("feedback")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"resume_text": dummy_resume, "job_description": dummy_job_description})
print(response["messages"][-1].content)
