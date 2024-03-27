from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import sqlite3

if sqlite3.sqlite_version_info < (3, 35, 0):
    # In Render, hotswap to pysqlite-binary if it's too old
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pysqlite3-binary"])
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

load_dotenv(override=True)


vector_store: Chroma | None = None


def chroma_init(persist_directory="./chroma_db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    collection_name = "issues"
    global vector_store
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )


chroma_init()
