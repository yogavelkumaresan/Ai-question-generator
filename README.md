# AI-Powered Question Generator from PDF

## Overview
This project is an AI-powered question generation system that automatically creates exam questions from PDF documents using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

The application extracts text from uploaded PDFs, stores semantic embeddings in ChromaDB, retrieves relevant content, and generates different types of questions using the Groq Llama 3.3 model.

---

## Features

- Upload PDF documents
- Automatic text extraction
- Semantic search using ChromaDB
- Generate Multiple Choice Questions (MCQs)
- Generate Fill in the Blank Questions
- Generate True or False Questions
- AI-generated explanations
- Interactive Streamlit interface

---

## Technologies Used

- Python
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq API
- Llama 3.3 70B
- PyMuPDF (fitz)

---

## Installation

Clone the repository

```bash
git clone https://github.com/yogavelkumaresan/Ai-question-generator.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Project Workflow

1. Upload PDF
2. Extract Text
3. Store Embeddings in ChromaDB
4. Retrieve Relevant Content
5. Generate Questions
6. Evaluate Answers
7. Display AI Explanation

---

## Future Improvements

- Difficulty Levels
- Multiple Language Support
- User Authentication
- Export Questions to PDF
- Analytics Dashboard

---

## Author

**Yogavel K**

M.Sc Data Science

