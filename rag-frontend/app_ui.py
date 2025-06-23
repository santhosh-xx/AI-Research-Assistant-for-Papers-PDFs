import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

# Page config
st.set_page_config(page_title="🧠 RAG Chatbot", layout="wide")
st.title("🧠 AI Research Assistant for Papers & PDFs")
st.caption("Powered by LLaMA3 (Ollama), FAISS & LangChain")

st.markdown("""
<style>
/* Input box styling */
div[data-baseweb="input"] input {
    background-color: white !important;
    color: black !important;
    font-weight: bold !important;
    font-size: 18px !important;
    font-family: 'Segoe UI', sans-serif !important;
}
.stTextInput > div > div > input {
    height: 50px !important;
}

/* Answer box */
.answer-box {
    background-color: #1c1c1c;
    color: white;
    padding: 1.2rem;
    border-radius: 10px;
    font-size: 24px;
    font-weight: 500;
    font-family: 'Segoe UI', sans-serif;
    margin-top: 0.5rem;
}

/* Top-right processing text */
#processing-msg {
    position: fixed;
    top: 20px;
    right: 15px;
    font-size: 24px;
    font-weight: 600;
    color: #4f4f4f;
    font-family: 'Segoe UI', sans-serif;
    background-color: #f1f1f1;
    padding: 0.4rem 1rem;
    border-radius: 8px;
    box-shadow: 0 0 6px rgba(0,0,0,0.1);
    z-index: 9999;
}

/* Extra large buttons */
.stButton > button {
    font-size: 22px !important;
    padding: 15px 30px !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    background-color: #0078d7 !important; /* Optional: customize color */
    color: white !important;
    transition: background-color 0.3s ease;
}

.stButton > button:hover {
    background-color: #005a9e !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📄 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("⏳ Processing..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
            )
        if response.status_code == 200:
            st.success("✅ Uploaded and processed successfully!")
        else:
            st.error("❌ Upload failed!")

# Clear history
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []

# Init history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Section
st.divider()
st.subheader("💬 Ask Your Document")

query = st.text_input("Enter your question", key="input", label_visibility="visible")

if st.button("Ask") and query:
    st.session_state.chat_history.append(("user", query))
    with st.spinner("Answering..."):
        try:
            res = requests.post(f"{API_URL}/ask", data={"question": query}, stream=True, timeout=120)
            answer = ""
            placeholder = st.empty()
            for chunk in res.iter_content(chunk_size=1024):
                decoded = chunk.decode("utf-8")
                answer += decoded
                placeholder.markdown(f"<div class='answer-box'>🤖 <strong>Bot:</strong> {answer}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append(("bot", answer))
        except requests.exceptions.ReadTimeout:
            st.error("⚠️ Backend timed out. Please try again.")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")

# Display History
st.divider()
st.subheader("🕓 Chat History")
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"🧑‍💼 **You:** {message}")
    else:
        st.markdown(f"<div class='answer-box'>🤖 <strong>Bot:</strong> {message}</div>", unsafe_allow_html=True)
