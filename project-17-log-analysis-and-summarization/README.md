# Project 17: Log Analyzer

## Purpose
This project demonstrates a log analyzer agent that can parse log files, identify errors, and summarize them using a language model. This is crucial for system monitoring and troubleshooting.

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
Automated log analysis can significantly reduce the time and effort required to identify and resolve system issues. This agent can provide immediate insights into system health, helping to prevent outages and improve operational efficiency.

## Extension Ideas
*   Integrate with real-time log streams (e.g., from ELK stack, Splunk).
*   Add anomaly detection capabilities to identify unusual patterns in logs.
*   Implement automated alerting based on critical error summaries.
