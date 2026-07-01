import streamlit as st
import fitz  
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

DB_PATH = "./chroma_db1"

@st.cache_resource
def get_vector_db():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    )

vector_db = get_vector_db()
groq = ChatGroq(api_key="Groq Api Key", model_name="llama-3.3-70b-versatile")

@st.cache_resource
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

def store_text_in_chroma(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = text_splitter.split_text(pdf_text)
    documents = [Document(page_content=chunk, metadata={"source": "pdf"}) for chunk in chunks]
    vector_db.add_documents(documents)
    vector_db.persist()

def retrieve_text_from_chroma(query):
    results = vector_db.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in results])

def generate_exam_questions_from_text(text, num_questions):
    prompt = f"""
You are an intelligent exam question generator.

Generate exactly {num_questions} diverse 1-mark questions based on the text below.

Include a random mix of:
- Multiple Choice Questions (MCQ) with 4 answer choices and mark the correct one.
- Fill in the blanks (single word or phrase).
- True or False questions — IMPORTANT: ensure a roughly equal number of 'True' and 'False' answers. Do NOT make all True/False answers 'False'. At least 40% of them should be 'True'.

Text:
{text}
"""
    return groq.invoke([HumanMessage(content=prompt)]).content.strip()
def explanation_generator(question, options, correct_answer):
    prompt = (
        f"Question: '{question}'\n"
        f"Options: {options}\n"
        f"Correct Answer: '{correct_answer}'\n\n"
        "➤ Explain why this is the correct answer.\n"
        "➤ Then explain why the other options are incorrect (if applicable).\n"
        "If this is a fill-in-the-blank or true/false question, explain based on that format."
    )
    return groq.invoke([HumanMessage(content=prompt)]).content.strip()

def parse_exam_question_output(question_text):
    questions = []
    lines = question_text.strip().split("\n")
    current = {"question": "", "type": "", "options": [], "answer": ""}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line[0].isdigit() and "." in line:
            if current["question"]:
                questions.append(current)
                current = {"question": "", "type": "", "options": [], "answer": ""}
            current["question"] = line.split(". ", 1)[1]

        elif any(line.startswith(opt) for opt in ["A)", "B)", "C)", "D)", "A.", "B.", "C.", "D."]):
            current["options"].append(line[3:].strip())
            current["type"] = "mcq"

        elif line.lower().startswith(("correct answer:", "answer:")):
            current["answer"] = line.split(":", 1)[1].strip()
            if not current["type"]:
                if current["answer"].lower() in ["true", "false"]:
                    current["type"] = "true_false"
                elif "___" in current["question"] or "blank" in current["question"].lower():
                    current["type"] = "fill_blank"
                else:
                    current["type"] = "short"

    if current["question"]:
        questions.append(current)

    return questions


st.title("Question Generator from PDF")

uploaded_file = st.file_uploader(" Upload a PDF file", type="pdf")
if uploaded_file and "pdf_uploaded" not in st.session_state:
    with st.spinner("Processing PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        store_text_in_chroma(pdf_text)
        st.success("PDF Uploaded & Stored Successfully!")
        st.session_state["pdf_uploaded"] = True

query = st.text_input(" Enter a topic or keyword for MCQs")
num_mcqs = st.number_input(" Enter the number of MCQs", min_value=1, max_value=30, value=5)

if st.button(" Generate Questions"):
    with st.spinner("Generating Questions..."):
        st.session_state.retrieved_text = retrieve_text_from_chroma(query)
        mcq_text = generate_exam_questions_from_text(st.session_state.retrieved_text, num_mcqs)
        st.session_state.mcq_data = parse_exam_question_output(mcq_text)
        st.session_state.current_question = 0
    st.success(" Questions Generated!")

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'explanations' not in st.session_state:
    st.session_state.explanations = {}

questions = st.session_state.get("mcq_data", [])
if st.session_state.current_question < len(questions):
    q_index = st.session_state.current_question
    q = questions[q_index]
    st.subheader(f"Q{q_index + 1}: {q['question']}")

    if q["type"] == "mcq":
        selected = st.radio("Choose an answer:", q["options"], key=f"q{q_index}")

    elif q["type"] == "fill_blank":
        selected = st.text_input("Fill in the blank:", key=f"q{q_index}")

    elif q["type"] == "true_false":
        selected = st.radio("Select True or False:", ["True", "False"], key=f"q{q_index}")
        q["options"] = ["True", "False"]
    else:
        selected = st.text_input("Answer:", key=f"q{q_index}")

    correct = q["answer"]

    if st.button(" Submit", key=f"submit_{q_index}"):
        if q["type"] == "mcq":
            correct = correct[2:]
        if selected.lower().strip() == correct.lower().strip():
            st.success(" Correct!")
        else:
            st.error(f" Wrong! Correct answer is: {correct}")

    if st.button(" Explain", key=f"explain_{q_index}"):
        if selected:
            exp_key = f"{q_index}-{selected}"
            if exp_key in st.session_state.explanations:
                explanation = st.session_state.explanations[exp_key]
            else:
                explanation = explanation_generator(q["question"], q.get("options", []), correct)
                st.session_state.explanations[exp_key] = explanation
            st.info(f" Explanation: {explanation}")
        else:
            st.warning(" Please submit an answer first!")

    if st.button(" Next", key=f"next_{q_index}"):
        st.session_state.current_question += 1
        st.rerun()
