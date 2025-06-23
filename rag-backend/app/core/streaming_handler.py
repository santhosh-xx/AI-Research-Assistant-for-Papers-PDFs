# app/core/streaming_handler.py
from langchain_core.callbacks.base import AsyncCallbackHandler

class StreamingResponseCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.queue.put(token)

    async def on_llm_end(self, *args, **kwargs):
        await self.queue.put("[[END]]")
