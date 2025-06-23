# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.core.loader import load_and_split
from app.core.embedder import get_embedder
from app.core.vector_store import create_and_save_vector_store, load_vector_store
from app.core.qa import create_qa_chain
from app.core.streaming_handler import StreamingResponseCallbackHandler
from langchain.memory import ConversationBufferMemory
import os
import asyncio
import queue

router = APIRouter()
VECTOR_DB_PATH = "vector_store/index"

session_memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
    output_key="result"
)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"docs/{file.filename}"
    os.makedirs("docs", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    documents = load_and_split(file_path)
    embedder = get_embedder()
    create_and_save_vector_store(documents, embedder)
    return {"status": "Document processed successfully"}

@router.post("/ask")
async def ask_question(question: str = Form(...)):
    embedder = get_embedder()
    vector_store = load_vector_store(embedder)

    # ✅ Use async queue for streaming
    token_queue: asyncio.Queue = asyncio.Queue()
    callback = StreamingResponseCallbackHandler(token_queue)

    qa = create_qa_chain(vector_store, memory=session_memory, callbacks=[callback])

    # ✅ Start QA in background
    async def run_chain():
        await qa.ainvoke({"query": question})

    # ✅ Streaming generator
    async def token_stream():
        task = asyncio.create_task(run_chain())
        while True:
            token = await token_queue.get()
            if token == "[[END]]":
                break
            yield token

        await task  # ensure completion

    return StreamingResponse(token_stream(), media_type="text/plain")
