# Project 15: Resume/Job-Match Bot

## Purpose
This project demonstrates a resume/job-match bot that compares a resume against a job description and provides a match score and feedback. It uses embeddings to represent the documents and a language model to generate human-readable feedback.

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
Automating the initial screening of resumes can significantly streamline the hiring process. This bot can quickly identify top candidates, saving recruiters time and ensuring that qualified applicants are not overlooked.

## Extension Ideas
*   Integrate with a real applicant tracking system (ATS).
*   Implement more sophisticated matching algorithms, considering skills, experience, and cultural fit.
*   Allow users to upload their resumes and job descriptions for personalized feedback.
