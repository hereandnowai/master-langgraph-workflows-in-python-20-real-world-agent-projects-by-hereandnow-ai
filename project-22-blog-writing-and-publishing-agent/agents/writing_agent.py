import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL

load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
model = MODEL

def writing_agent(state):
    """
    Writes an SEO-optimized blog post based on the selected topic.
    """
    print("--- WRITING AGENT ---")
    selected_topic = state["selected_topic"]
    organization_name = state["organization_name"]
    organization_description = state["organization_description"]
    
    llm = ChatGoogleGenerativeAI(
        model=model, 
        temperature=0.7, 
        google_api_key=google_api_key
    )
    
    prompt = f"""
    You are an expert SEO content writer for the company: {organization_name}.
    Company Description: {organization_description}.
    
    Your task is to write a comprehensive, engaging, and SEO-optimized blog post on the following topic:
    "{selected_topic}"
    
    Please adhere to the latest SEO best practices for 2025, including:
    - Use the main keyword phrase naturally throughout the article.
    - Include related LSI keywords.
    - Write a compelling meta title and meta description.
    - Use headings (H1, H2, H3) to structure the content.
    - Write an introduction that hooks the reader and a conclusion that summarizes the key points.
    - Ensure the article is at least 800 words long.
    
    The tone should be professional, informative, and engaging.
    """
    
    try:
        response = llm.invoke(prompt)
        print("   > Successfully wrote the blog post.")
        return {"blog_post": response.content}
    except Exception as e:
        print(f"   > Error during writing: {e}")
        return {"blog_post": ""}
