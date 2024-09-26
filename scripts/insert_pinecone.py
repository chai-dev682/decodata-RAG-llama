from pinecone import Pinecone
from pinecone import ServerlessSpec
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from config import load_env
import os
import time

load_env()

from src.tools import pdf_tools

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
dims = 1536
spec = ServerlessSpec(
    cloud="aws", region="us-east-1"
)

embed_model = OpenAIEmbedding(openai_api_key=os.environ["OPENAI_API_KEY"])

def check_name(star_list, target):
    """Checks if a dictionary in the list has a specific name."""
    for item in star_list:
        if item['name'] == target:
            return True
    return False

# check if index already exists (it shouldn't if this is first time)
if not check_name(pc.list_indexes().indexes, os.environ["PINECONE_INDEX_NAME"]):
    # if it does not exist, create index
    pc.create_index(
        name=os.environ["PINECONE_INDEX_NAME"],
        dimension=dims,  # dimensionality of embed 3
        metric='cosine',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(os.environ["PINECONE_INDEX_NAME"]).status['ready']:
        time.sleep(1)

# connect to index
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

# Initialize VectorStore
vector_store = PineconeVectorStore(pinecone_index=index)

# Our pipeline with the addition of our PineconeVectorStore
pipeline = IngestionPipeline(
    transformations=[
        SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=95,
            embed_model=embed_model,
            ),
        embed_model,
        ],
        vector_store=vector_store  # Our new addition
    )

# run pipeline
pipeline.run(documents=pdf_tools.parse_pdfs_with_subdirectory_metadata("../fixtures/hierarchies"))

print(index.describe_index_stats())