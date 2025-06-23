import re
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    # Basic NLP cleaning
    text = text.lower()  # lowercasing
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove special chars

    tokens = nltk.word_tokenize(text)
    cleaned = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(cleaned)

def load_and_split(pdf_path: str):
    # Load and extract PDF text
    with fitz.open(pdf_path) as doc:
        raw_text = ""
        for page in doc:
            raw_text += page.get_text()

    cleaned_text = clean_text(raw_text)

    # Create one document object with the cleaned text
    langchain_doc = Document(page_content=cleaned_text, metadata={"source": pdf_path})

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents([langchain_doc])
