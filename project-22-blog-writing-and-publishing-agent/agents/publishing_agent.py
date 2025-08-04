import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import re
import markdown

def publishing_agent(state):
    """
    Publishes the final blog post to WordPress.
    """
    print("--- PUBLISHING AGENT ---")
    final_blog_post = state["final_blog_post"]
    
    # Clean the post of markdown fences and other artifacts
    cleaned_post = final_blog_post.strip()
    # Remove ```html, ```markdown, or ```
    cleaned_post = re.sub(r'^```(html|markdown)?\s*', '', cleaned_post, flags=re.IGNORECASE)
    cleaned_post = re.sub(r'\s*```$', '', cleaned_post)
    cleaned_post = cleaned_post.strip()

    lines = cleaned_post.split('\n')
    post_title = "Automated Blog Post"
    post_content = cleaned_post

    # Find title (H1 in markdown)
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            post_title = stripped_line.lstrip('# ').strip()
            post_content = '\n'.join(lines[i+1:]).strip()
            break
    else: # if no H1 title is found
        # Use the first non-empty line as title
        for i, line in enumerate(lines):
            if line.strip():
                post_title = line.strip()
                post_content = '\n'.join(lines[i+1:]).strip()
                break

    # Convert markdown to HTML
    html_content = markdown.markdown(post_content)

    wp_url = os.getenv("WORDPRESS_URL")
    wp_username = os.getenv("WORDPRESS_USERNAME")
    wp_password = os.getenv("WORDPRESS_PASSWORD")
    
    if not all([wp_url, wp_username, wp_password]):
        print("   > WordPress credentials not found in .env file.")
        return {"published": False}
        
    client = Client(wp_url, wp_username, wp_password)
    
    post = WordPressPost()
    post.title = post_title
    post.content = html_content
    post.post_status = 'publish'
    
    try:
        client.call(NewPost(post))
        print(f"   > Successfully published the blog post: {post_title}")
        return {"published": True}
    except Exception as e:
        print(f"   > Error publishing to WordPress: {e}")
        return {"published": False}
