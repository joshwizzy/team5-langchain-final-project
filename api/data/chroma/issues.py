from langchain.docstore.document import Document

from .init import vector_store


def create_embeddings(chunks):
    vector_store.add_documents(chunks)


def similarity_search(query: str) -> list[Document]:
    docs = vector_store.similarity_search_with_score(query, 4)
    docs = [doc[0] for doc in docs]
    return docs
