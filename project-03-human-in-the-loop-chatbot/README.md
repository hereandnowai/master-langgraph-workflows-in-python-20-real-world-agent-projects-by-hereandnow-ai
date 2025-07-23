# Project 3: Memory-Enabled Agent

## Purpose
This project demonstrates how to add memory to a LangGraph agent. The agent can remember previous turns in the conversation and use that context to inform its responses.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt

        python3 -m .venv venv
    source venv/bin/activate
    pip install langchain langchain-community langchain-core langchain-chat llama_index duckduckgo-search langgraph
    ```
2.  **Run the agent:**
    ```bash
    python main.py
    ```

## Business Value
Memory is essential for creating natural and engaging conversational experiences. A memory-enabled agent can provide more personalized and helpful responses, leading to higher customer satisfaction and better user engagement.

## Extension Ideas
*   Use a more persistent memory backend, such as a database or a file.
*   Implement a more sophisticated memory management strategy to handle long conversations.
*   Explore different types of memory, such as short-term and long-term memory.
