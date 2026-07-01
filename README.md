# AI-Powered Question Generator from PDF

## Overview

AI-Powered Question Generator is a Streamlit-based application that automatically generates exam questions from PDF documents using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

The system extracts text from uploaded PDF files, stores document embeddings in ChromaDB, retrieves relevant content using semantic search, and generates intelligent questions using the Groq Llama 3.3 model.

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

## Project Workflow

1. Upload a PDF document
2. Extract text from the PDF
3. Store embeddings in ChromaDB
4. Retrieve relevant content
5. Generate AI-based questions
6. Evaluate user answers
7. Display explanations

---

## Installation

Clone the repository

```bash
git clone https://github.com/yogavelkumaresan/Ai-question-generator.git
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Future Enhancements

- Multi-language support
- Difficulty level selection
- User authentication
- Export questions to PDF
- Performance analytics dashboard

---

## Author

**Yogavel K**

M.Sc Data Science

LinkedIn:
https://linkedin.com/in/yogavel-k-94096431a

Email:
yogavel210@gmail.com
