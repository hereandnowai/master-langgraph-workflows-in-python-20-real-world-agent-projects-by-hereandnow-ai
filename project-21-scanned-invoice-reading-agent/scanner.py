import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, Field # data validation and serialization | automatically checks and converts input types
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from pypdf import PdfReader
from config import MODEL

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = MODEL

# --- Rate Limiter ---
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10 seconds
    check_every_n_seconds=0.1,
    max_bucket_size=10,
)

# --- State Definition ---
# Define the structure of the data that will be passed between nodes in the graph.
class GraphState(TypedDict):
    invoice_path: str # The path to the invoice PDF file
    invoice_text: str  # The raw text from the invoice
    structured_data: Annotated[dict, "Structured invoice data in JSON format"]

# --- Pydantic Model for Structured Data ---
# Define the data structure Gemini should extract.
class Invoice(BaseModel):
    """Model to hold structured data extracted from an invoice."""
    vendor_name: str = Field(..., description="The name of the company issuing the invoice.")
    customer_name: str = Field(..., description="The name of the customer on the invoice.")
    invoice_number: str = Field(..., description="The unique identifier for the invoice.")
    total_amount: float = Field(..., description="The total amount due on the invoice.")
    due_date: str = Field(..., description="The date when the invoice payment is due.")

# --- Nodes ---
# Each node in the graph is a function or a runnable.

def read_invoice_file(state: GraphState) -> GraphState:
    """Reads the raw text from the invoice file."""
    print("--- 1. READING INVOICE FILE ---")
    reader = PdfReader(state["invoice_path"])
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print("   > Successfully read text.")
    return {"invoice_text": text}

def extract_structured_data(state: GraphState) -> GraphState:
    """Extracts structured data from the invoice text using Google Gemini."""
    print("--- 2. EXTRACTING STRUCTURED DATA ---")
    
    # Initialize the Google Gemini model with the desired output structure
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=google_api_key, temperature=0, rate_limiter=rate_limiter)
    structured_llm = llm.with_structured_output(Invoice)

    prompt = f"""
    You are an expert accounting assistant.
    Analyze the following invoice text and extract the key details into the required JSON format.
    
    Invoice Text:
    ---
    {state['invoice_text']}
    ---
    """
    
    # Invoke the model to get the structured data
    print("   > Calling Gemini API...")
    response = structured_llm.invoke(prompt)
    
    print("   > Successfully extracted data with Gemini.")
    return {"structured_data": response.dict()}

# --- Graph Definition ---
workflow = StateGraph(GraphState)

# Add the nodes to the graph
workflow.add_node("read_file", read_invoice_file)
workflow.add_node("extract_data", extract_structured_data)

# Set the entry point of the graph
workflow.set_entry_point("read_file")

# Add edges to define the flow
workflow.add_edge("read_file", "extract_data")
workflow.add_edge("extract_data", END)

# Compile the graph into a runnable object
app = workflow.compile()

# --- Run the Graph ---
if __name__ == "__main__":
    print("Starting Invoice Processing Workflow...")
    # Construct the absolute path to the invoice file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    invoice_path = os.path.join(script_dir, "invoice01.pdf")
    
    # The initial state now requires the path to the invoice PDF
    initial_state = {"invoice_path": invoice_path}
    final_state = app.invoke(initial_state)
    
    print("\n--- EXTRACTION COMPLETE ---")
    print("Final structured data:")
    import json
    print(json.dumps(final_state['structured_data'], indent=2))