# Project 19: Command-Line Tool Agent

## Purpose
This project demonstrates a command-line tool agent that can execute shell commands and then summarize their output. This allows an AI agent to interact with the underlying operating system.

## Setup & Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up your Google API key:**
    ```bash
    export GOOGLE_API_KEY=your_api_key
    ```
3.  **Run the agent:**
    ```bash
    python main.py
    ```

## Business Value
Automating command-line tasks can be incredibly powerful for system administration, development operations, and data processing. This agent can perform tasks like file management, software installation, or data extraction, reducing manual effort and potential for human error.

## Extension Ideas
*   Implement a more robust command execution tool with error handling and timeouts.
*   Allow the LLM to dynamically choose which commands to run based on user requests.
*   Integrate with a remote server to manage infrastructure.
