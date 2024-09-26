from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
import os


pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

# Initialize VectorStore
vector_store = PineconeVectorStore(pinecone_index=index)

# Instantiate VectorStoreIndex object from your vector_store object
vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

def query_pinecone(query: str, top_k = 5):
    # Grab top_k search results
    retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=top_k)

    query_engine = RetrieverQueryEngine(retriever=retriever)

    llm_query = query_engine.query(query)

    return llm_query.response
