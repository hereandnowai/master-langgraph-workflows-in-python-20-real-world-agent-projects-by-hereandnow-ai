# LangGraph Tutorial: Master AI Agent Workflows with Python & Google Gemini

![HERE AND NOW AI Logo](https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/HNAI%20Title%20-Teal%20%26%20Golden%20Logo%20-%20DESIGN%203%20-%20Raj-07.png)

## Unlock the Power of AI Agents with HERE AND NOW AI

Welcome to the definitive **LangGraph tutorial** repository, meticulously crafted by **HERE AND NOW AI** – *designed with passion for innovation*. This comprehensive guide features **20 compact, real-world AI agent projects** built with Python (≥3.9), **LangGraph v0.5.3**, and the latest **LangChain integrations** for Google Gemini models (specifically `gemini-2.5-flash`). Our focus is on providing **beginner-friendly** yet powerful examples to help you achieve **mastery** in building stateful, multi-actor AI applications.

Each project is designed to be a standalone learning module, covering essential LangGraph concepts and demonstrating practical applications across various domains like finance, HR, marketing, and multi-agent orchestration. We ensure all methods are up-to-date, avoiding deprecated functionalities.

## About HERE AND NOW AI

At HERE AND NOW AI, we are dedicated to empowering developers and businesses with cutting-edge AI solutions and educational resources. Our mission is to bridge the gap between complex AI theory and practical, real-world implementation. Connect with us:

*   **Website:** [https://hereandnowai.com](https://hereandnowai.com)
*   **Email:** [info@hereandnowai.com](mailto:info@hereandnowai.com)
*   **Phone:** +91 996 296 1000
*   **Blog:** [https://hereandnowai.com/blog](https://hereandnowai.com/blog)
*   **LinkedIn:** [HERE AND NOW AI on LinkedIn](https://www.linkedin.com/company/hereandnowai/)
*   **Instagram:** [@hereandnow_ai](https://instagram.com/hereandnow_ai)
*   **GitHub:** [HERE AND NOW AI on GitHub](https://github.com/hereandnowai)
*   **X (Twitter):** [@hereandnow_ai](https://x.com/hereandnow_ai)
*   **YouTube:** [@hereandnow_ai](https://youtube.com/@hereandnow_ai)

## Environment Setup

To get started with any of the projects, follow these steps:

1.  **Create a virtual environment:**
    ```bash
    python3.9 -m venv venv
    source venv/bin/activate
    ```

2.  **Install common dependencies:**
    All necessary libraries for all projects are consolidated in the root `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys:**
    Many projects require API keys for Google Gemini (for `langchain-google-genai`) and/or Tavily (for search tools). Set them as environment variables:
    ```bash
    export GOOGLE_API_KEY=your_google_api_key
    export TAVILY_API_KEY=your_tavily_api_key # Only if the project uses search tools
    ```

## Directory Structure

```
langgraph-tutorial/
  GEMINI.md
  branding.json
  README.md
  requirements.txt # Consolidated requirements for all projects
  project01/
    README.md
    main.py
    # project-specific requirements.txt (now optional, but kept for individual project clarity)
  ...
  project20/
    README.md
    main.py
    # project-specific requirements.txt (now optional, but kept for individual project clarity)
```

## Coding & Documentation Guidelines

All code adheres to **PEP-8**, includes type hints, and follows industry-standard LangChain/LangGraph conventions. Each `main.py` file is kept concise (≤ 20 lines) with clear inline comments for readability.

Each project folder includes:

*   `main.py`: The core LangGraph agent implementation.
*   `README.md`: Outlines the project's purpose, setup & usage, business value, and extension ideas.

## Project List: Your Path to LangGraph Mastery

Here's a brief overview of the 20 projects, designed to progressively build your skills in **AI agent development**:

1.  **Basic Chat Agent**: Simple state graph for foundational understanding.
2.  **Tools Integration**: Fetch live data via function nodes, enhancing agent capabilities.
3.  **Memory-Enabled Agent**: Intermediate state tracking for contextual conversations.
4.  **Human-in-the-Loop**: Approval node using `interrupt` for critical oversight.
5.  **Conditional Edges**: Branches based on numeric thresholds for dynamic workflows.
6.  **Deferred Nodes**: Map-reduce style aggregation for efficient data processing.
7.  **Node-Level Caching**: Reduce redundant model calls, optimizing performance and cost.
8.  **Finance Assistant**: Graph agent querying stock prices for real-time financial insights.
9.  **Marketing Generator**: Cycle to refine slogans, boosting creative content generation.
10. **HR Policy Helper**: Stateful Q&A from document, streamlining HR support.
11. **Multi-Agent Workflow**: Agents coordinate via graph for complex task automation.
12. **Email Parser + Responder**: Tool invocation graph for automated communication.
13. **Interview Coach**: Retrieve, assess candidate responses, aiding recruitment.
14. **Budget Planner**: CSV input → summary graph for financial management.
15. **Resume/Job-Match Bot**: Multi-node compare graph for talent acquisition.
16. **QA over Knowledge Base**: Integrate vector DB for intelligent information retrieval.
17. **Log Analyzer**: Parse logs, summarize errors for system health monitoring.
18. **Report Generator**: Fetch and compile insights for automated reporting.
19. **Command-Line Tool Agent**: Shell command node for system interaction.
20. **Capstone Unified Assistant**: Finance + HR + Marketing orchestration – a powerful, integrated AI solution.

## Business Value & Pro Tips

Each project's `README.md` includes a dedicated "Business Value" section, highlighting how the agent supports real-world domains. We also suggest future enhancements, such as GUI integration, database integration, or deployment to platforms like LangGraph Cloud, to inspire further development.

## How to Run

To run any specific project, navigate to its directory (e.g., `langgraph-tutorial/project01`), ensure your environment variables for API keys are set, and then execute `python main.py`.

**Start your journey to LangGraph mastery with HERE AND NOW AI today!**
