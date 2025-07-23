import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

def publishing_agent(state):
    """
    Publishes the final blog post to WordPress.
    """
    print("--- PUBLISHING AGENT ---")
    final_blog_post = state["final_blog_post"]
    selected_topic = state["selected_topic"]
    
    wp_url = os.getenv("WORDPRESS_URL")
    wp_username = os.getenv("WORDPRESS_USERNAME")
    wp_password = os.getenv("WORDPRESS_PASSWORD")
    
    if not all([wp_url, wp_username, wp_password]):
        print("   > WordPress credentials not found in .env file.")
        return {"published": False}
        
    client = Client(wp_url, wp_username, wp_password)
    
    post = WordPressPost()
    post.title = selected_topic
    post.content = final_blog_post
    post.post_status = 'publish'
    
    try:
        client.call(NewPost(post))
        print(f"   > Successfully published the blog post: {selected_topic}")
        return {"published": True}
    except Exception as e:
        print(f"   > Error publishing to WordPress: {e}")
        return {"published": False}
