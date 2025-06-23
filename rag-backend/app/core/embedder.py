from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_embedder():
    """
    Returns a SentenceTransformer-based embedder using a free, high-quality model.
    """
    model_name = "sentence-transformers/all-mpnet-base-v2"
    return SentenceTransformerEmbeddings(model_name=model_name)
