import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agents.research_agent import research_agent
from agents.writing_agent import writing_agent
from agents.proofreading_agent import proofreading_agent
from agents.publishing_agent import publishing_agent
from config import ORGANIZATION_NAME, ORGANIZATION_DESCRIPTION

# Load environment variables
load_dotenv()

# --- State Definition ---
class GraphState(TypedDict):
    organization_name: str
    organization_description: str
    urls: List[str]
    research_results: str
    blog_post: str
    final_blog_post: str
    published: bool

# --- Graph Definition ---
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("research", research_agent)
workflow.add_node("write", writing_agent)
workflow.add_node("proofread", proofreading_agent)
workflow.add_node("publish", publishing_agent)

# Add edges
workflow.set_entry_point("research")
workflow.add_edge("research", "write")
workflow.add_edge("write", "proofread")
workflow.add_edge("proofread", "publish")
workflow.add_edge("publish", END)

# --- App ---
app = workflow.compile()

# --- Main Execution ---
if __name__ == "__main__":
    # Set initial state with URLs for research
    initial_state = {
        "organization_name": ORGANIZATION_NAME,
        "organization_description": ORGANIZATION_DESCRIPTION,
        "urls": [
            "https://developers.googleblog.com/en/introducing-opal/"
        ],
    }
    
    print("\n--- STARTING BLOG WRITING WORKFLOW ---")
    print(f"Organization: {initial_state['organization_name']}")
    print(f"URLs for research: {initial_state['urls']}")
    
    # Run the full workflow
    final_state = app.invoke(initial_state)
    
    print("\n--- BLOG POST PUBLISHED ---")
    print(f"Final Status: {'Success' if final_state.get('published') else 'Failed'}")