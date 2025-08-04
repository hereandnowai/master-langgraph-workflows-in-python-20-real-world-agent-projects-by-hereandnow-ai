import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = MODEL

def proofreading_agent(state):
    """
    Proofreads and refines the generated blog post.
    """
    print("--- PROOFREADING AGENT ---")
    blog_post = state["blog_post"]
    
    llm = ChatGoogleGenerativeAI(
        model=model, 
        temperature=0, 
        google_api_key=google_api_key
    )
    
    prompt = f"""
    You are an expert proofreader and editor.
    Your task is to review the following blog post for any grammatical errors, spelling mistakes, or awkward phrasing.
    Please also ensure the article is clear, concise, and easy to read.
    
    Blog Post:
    ---
    {blog_post}
    ---
    
    Return the polished, final version of the blog post as a single block of markdown text. Do not include any HTML tags or code blocks.
    """
    
    try:
        response = llm.invoke(prompt)
        print("   > Successfully proofread the blog post.")
        return {"final_blog_post": response.content}
    except Exception as e:
        print(f"   > Error during proofreading: {e}")
        return {"final_blog_post": blog_post}
