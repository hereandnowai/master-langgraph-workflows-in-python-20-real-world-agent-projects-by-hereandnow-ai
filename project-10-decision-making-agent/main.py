

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

# Create a dummy document
doc = "Our company's vacation policy allows for 20 days of paid time off per year."

# Create a vector store
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(doc)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()

# Define the chatbot
def chatbot(state: State):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Create the graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.set_finish_point("chatbot")

# Compile and run the graph
app = graph.compile()
response = app.invoke({"messages": [("human", "How many vacation days do I get?")]})
print(response["messages"][-1].content)

