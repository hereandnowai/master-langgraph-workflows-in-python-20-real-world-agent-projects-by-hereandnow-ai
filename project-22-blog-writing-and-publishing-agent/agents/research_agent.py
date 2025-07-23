from config import BLOG_TOPICS

def research_agent(state):
    """
    Returns a list of blog post topics from the config file.
    """
    print("--- RESEARCH AGENT ---")
    print("   > Loaded topics from config file.")
    return {"research_results": BLOG_TOPICS}
