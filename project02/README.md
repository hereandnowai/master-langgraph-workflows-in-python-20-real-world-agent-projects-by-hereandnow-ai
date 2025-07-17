# Project 2: Tools Integration

## Purpose
This project demonstrates how to integrate external tools into a LangGraph agent. The agent can use a search tool to fetch live data from the internet and incorporate it into its response.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your Tavily API key:**
    ```bash
    export TAVILY_API_KEY=your_api_key
    ```
3.  **Run the agent:**
    ```bash
    python main.py
    ```

## Business Value
Agents with tool integration can access real-time information, making them much more powerful. This is crucial for applications in finance (stock prices), e-commerce (product availability), or any domain that requires up-to-date information.

## Extension Ideas
*   Add more tools, such as a calculator or a calendar.
*   Implement a tool-selection mechanism to allow the agent to choose the best tool for a given task.
*   Use a more sophisticated tool-calling implementation to handle complex tool inputs and outputs.
