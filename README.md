# 🧠 RAG-Based AI Document Assistant

A powerful AI chatbot that reads, understands, and answers questions from uploaded documents using **RAG (Retrieval-Augmented Generation)**, **FAISS**, **LangChain**, **LLaMA3 (via Ollama)**, and a clean **Streamlit UI**.

---

## 🚀 Features

- 📄 Upload and read documents (PDFs)
- 🤖 Ask questions about the content
- 💡 Structured and concise answers
- 🔁 Chat history and context-aware memory
- ⏱️ Real-time streaming responses
- 🎨 Styled frontend with dark/light UI enhancements

---

## 🧰 Tech Stack

| Layer      | Tech Used                                |
|------------|------------------------------------------|
| Backend    | FastAPI, LangChain, FAISS, Ollama        |
| Embeddings | SentenceTransformers / HuggingFace       |
| LLM        | LLaMA3 via Ollama                        |
| Frontend   | Streamlit                                |

---


# 🧑‍💻 Getting Started (Local Development)


1. Clone the repo

git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot

2. Setup Python Environment

python -m venv env
Windows: .\env\Scripts\activate

3. Install Dependencies

For Backend:

cd rag-backend
pip install -r requirements.txt

For Frontend:

cd ../rag-frontend
pip install -r requirements.txt

4. Install & Run Ollama (LLM Server)
Install Ollama from https://ollama.com, then run:

ollama run llama3

Let Ollama run in background — it powers your LLM.

🚦 Run the App
1. Start the Backend

cd rag-backend
uvicorn app.main:app --reload

2. Start the Frontend

cd ../rag-frontend
streamlit run app_ui.py

Access app at http://localhost:8501


🧪 Usage

Upload a PDF in the sidebar.

Ask your question in the chat.

The model retrieves relevant chunks, processes them, and responds.

Chat history is shown with structured formatting.

Use “Clear Chat History” to reset memory.


🌐 Author
Santhosh
Passionate about building smart assistants and intelligent tools.
GitHub: santhosh-xx
