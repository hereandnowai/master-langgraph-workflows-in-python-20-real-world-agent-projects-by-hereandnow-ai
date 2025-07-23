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

## Purpose
This project demonstrates how to incorporate a human-in-the-loop for approval or feedback. The graph will pause and wait for user input before continuing, which is critical for tasks that require human oversight.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the agent:**
    ```bash
    python main.py
    ```
    The application will prompt you for input in the terminal.

## Business Value
Human-in-the-loop workflows are essential for preventing errors and ensuring quality in automated systems. This is particularly important in domains like finance (approving transactions), healthcare (verifying diagnoses), and content moderation (reviewing flagged content).

## Extension Ideas
*   Implement a more sophisticated approval mechanism using LangGraph's `interrupt` feature.
*   Build a simple web interface for the human approval step.
*   Add a timeout to the human input, so the process can continue automatically if no input is received.
