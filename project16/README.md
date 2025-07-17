# Project 16: QA over Knowledge Base

## Purpose
This project demonstrates a Question-Answering (QA) agent that can answer questions based on a provided knowledge base. It integrates a vector database to retrieve relevant information and a language model to formulate the answer.

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
Providing instant, accurate answers to common questions from a knowledge base can significantly improve customer support, internal training, and information retrieval within an organization. This reduces the need for human intervention for routine queries.

## Extension Ideas
*   Connect to a larger, real-world knowledge base (e.g., company documentation, product manuals).
*   Implement a feedback mechanism for users to rate the quality of answers.
*   Add a human escalation path for questions that cannot be answered by the agent.
