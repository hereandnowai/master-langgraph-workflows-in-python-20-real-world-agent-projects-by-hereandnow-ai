# Project 13: Interview Coach

## Purpose
This project demonstrates an interview coach agent that can retrieve assessment criteria and evaluate candidate responses. It uses a vector store to store criteria and a language model to assess the input.

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
Automating parts of the interview process can save significant time for HR and hiring managers. This agent can provide consistent, objective initial assessments, allowing human reviewers to focus on more nuanced aspects of candidate evaluation.

## Extension Ideas
*   Integrate with a real-time interview platform to assess responses as they are given.
*   Expand the knowledge base with more detailed assessment rubrics for various roles.
*   Add a feedback mechanism for candidates based on their performance.
