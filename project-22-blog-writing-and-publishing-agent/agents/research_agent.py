import os
from langchain_tavily import TavilySearch

def research_agent(state):
    """
    Uses the Tavily search tool to get the content from the given URLs.
    """
    print("--- RESEARCH AGENT ---")
    urls = state.get("urls", [])
    if not urls:
        print("   > No URLs provided for research.")
        return {"research_results": ""}

    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        print("   > Tavily API key not found in .env file.")
        return {"research_results": ""}

    tool = TavilySearch(api_key=tavily_api_key)

    all_content = ""
    for url in urls:
        try:
            # Use Tavily to get the content of the URL
            results = tool.invoke(f"get_contents:{url}")
            all_content += f"--- Content from {url} ---\n{results}\n\n"
            print(f"   > Fetched content from {url}")
        except Exception as e:
            print(f"   > Error fetching content from {url}: {e}")

    research_file_path = "project-22-blog-writing-and-publishing-agent/research_results.txt"
    with open(research_file_path, "w") as f:
        f.write(all_content)

    print(f"   > Research results written to {research_file_path}")
    return {"research_results": research_file_path}
