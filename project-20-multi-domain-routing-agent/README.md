# Project 20: Capstone Unified Assistant

## Purpose
This capstone project integrates concepts from previous projects to create a unified assistant capable of handling finance, HR, and marketing queries. It demonstrates advanced routing and orchestration of multiple specialized agents within a single LangGraph workflow.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your Google API key and Tavily API key:**
    ```bash
    export GOOGLE_API_KEY=your_api_key
    export TAVILY_API_KEY=your_api_key
    ```
3.  **Run the agent:**
    ```bash
    python main.py
    ```

## Business Value
A unified assistant can serve as a central point of contact for various business functions, improving efficiency and user experience. Instead of interacting with separate systems for finance, HR, or marketing, users can get comprehensive support from a single intelligent agent, streamlining operations and reducing friction.

## Extension Ideas
*   Implement more sophisticated routing mechanisms, possibly using an LLM to decide the best agent.
*   Integrate with real-world APIs for each domain (e.g., financial APIs, HRIS systems, marketing platforms).
*   Add a user interface to make the assistant more accessible and interactive.
*   Expand to include more domains, such as IT support, legal, or sales.
