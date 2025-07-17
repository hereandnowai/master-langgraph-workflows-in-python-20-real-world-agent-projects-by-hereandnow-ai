# Project 7: Node-Level Caching

## Purpose
This project demonstrates how to use node-level caching to reduce redundant model calls in a LangGraph agent. The agent will cache the results of a node and reuse them if the same input is received again.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the agent:**
    ```bash
    python main.py
    ```

## Business Value
Caching is a powerful technique for improving performance and reducing costs. In agentic workflows, it can be used to avoid expensive model calls, API requests, or database queries. This can lead to significant savings in both time and money.

## Extension Ideas
*   Use a more persistent cache, such as a database or a file.
*   Implement a more sophisticated caching strategy, such as time-based expiration or least-recently-used (LRU) eviction.
*   Explore how to use caching in combination with other LangGraph features, such as conditional edges and deferred nodes.
