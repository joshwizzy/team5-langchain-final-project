import hashlib

from langchain.docstore.document import Document

from .init import vector_store


def compute_hash(chunk):
    chunk_hash = hashlib.sha256(chunk.page_content.encode()).hexdigest()
    return chunk_hash


def create_embeddings(chunks):
    ids = [compute_hash(chunk) for chunk in chunks]
    vector_store.add_documents(chunks, ids=ids, add_to_docstore=False)


def similarity_search(query: str) -> list[Document]:
    docs = vector_store.similarity_search_with_score(query, k=4)

    # scores = [doc[1] for doc in docs]
    docs = [doc[0] for doc in docs]
    return docs
