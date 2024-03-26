from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


load_dotenv(override=True)


vector_store: Chroma | None = None


def chroma_init(persist_directory="./chroma_db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    collection_name = "issues"
    global vector_store
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )


chroma_init()
