import os
import random
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agents.research_agent import research_agent
from agents.writing_agent import writing_agent
from agents.proofreading_agent import proofreading_agent
from agents.publishing_agent import publishing_agent
from config import ORGANIZATION_NAME, ORGANIZATION_DESCRIPTION, BLOG_TOPICS

# Load environment variables
load_dotenv()

# --- State Definition ---
class GraphState(TypedDict):
    organization_name: str
    organization_description: str
    topic: str
    research_results: List[str]
    selected_topic: str
    blog_post: str
    final_blog_post: str
    published: bool

# --- Node Functions ---
def select_topic_node(state):
    """
    Node for the user to select a blog topic from the research results.
    """
    print("\n--- TOPIC SELECTION ---")
    if not state.get("research_results"):
        print("No research results found. Exiting.")
        return {"selected_topic": "No topic selected"}

    for i, topic in enumerate(state["research_results"]):
        print(f"{i+1}. {topic}")

    while True:
        try:
            selection = int(input(f"Please select a topic to write about (1-{len(state['research_results'])}): "))
            if 1 <= selection <= len(state["research_results"]):
                selected = state["research_results"][selection-1]
                print(f"   > You selected: {selected}")
                return {"selected_topic": selected}
            else:
                print(f"Invalid selection. Please choose a number between 1 and {len(state['research_results'])}.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

# --- Graph Definition ---
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("research", research_agent)
workflow.add_node("select_topic", select_topic_node)
workflow.add_node("write", writing_agent)
workflow.add_node("proofread", proofreading_agent)
workflow.add_node("publish", publishing_agent)

# Add edges
workflow.set_entry_point("research")
workflow.add_edge("research", "select_topic")
workflow.add_edge("select_topic", "write")
workflow.add_edge("write", "proofread")
workflow.add_edge("proofread", "publish")
workflow.add_edge("publish", END)

# --- App ---
app = workflow.compile()

# --- Main Execution ---
if __name__ == "__main__":
    # Set initial state from config
    initial_state = {
        "organization_name": ORGANIZATION_NAME,
        "organization_description": ORGANIZATION_DESCRIPTION,
        "topic": random.choice(BLOG_TOPICS),
    }
    
    print("--- STARTING BLOG WRITING WORKFLOW ---")
    print(f"Organization: {initial_state['organization_name']}")
    print(f"Topic: {initial_state['topic']}")
    
    # Run the full workflow
    final_state = app.invoke(initial_state)
    
    print("\n--- BLOG POST PUBLISHED ---")
    print(f"Final Status: {'Success' if final_state.get('published') else 'Failed'}")
