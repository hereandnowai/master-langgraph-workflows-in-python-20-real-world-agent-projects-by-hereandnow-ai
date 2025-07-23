# Project 22: Blog Writing and Publishing Agent

This project demonstrates a multi-agent workflow for writing, proofreading, and publishing a blog post to a WordPress website. The agent uses a configuration file for the organization's details and a list of predefined blog topics.

## Workflow

1.  **Topic Selection**: The application randomly selects a topic from the `config.py` file.
2.  **Research Agent**: This agent loads the predefined blog topics from the `config.py` file.
3.  **Human-in-the-Loop**: The user is prompted to select one of the topics for the blog post.
4.  **Writing Agent**: Once the topic is confirmed, this agent writes a complete, SEO-optimized blog post, following the latest best practices for 2025.
5.  **Proofreading Agent**: The generated article is passed to this agent, which reviews, edits, and refines the content for quality, clarity, and correctness.
6.  **Publishing Agent**: The final, polished article is sent to this agent, which connects to the user's WordPress site and publishes it as a new post.

## Setup

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Create a `.env` file and add your credentials:
    ```bash
    cp .env.example .env
    ```
3.  Run the application:
    ```bash
    python app.py
    ```
