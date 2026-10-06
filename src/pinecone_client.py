from pinecone import Pinecone

from src.config import (PINECONE_API_KEY,PINECONE_INDEX_NAME,PINECONE_NAMESPACE)


#creating Pinecone client

pc = Pinecone(
    api_key=PINECONE_API_KEY
)


#Index Connection 

index =  pc.index(
    PINECONE_INDEX_NAME
)




#function for basic information about the stats
def get_index_stats():
    """
    Get basic statistics of the Pinecone index.
    """

    stats = index.describe_index_stats()
    return stats


#Function for serching the chunks form pinepone index

def search_pinecone(
        query_embedding : list[float],
        top_k : int = 5):

    """
    Search the existing Pinecone knowledge base
    using the query embedding.
    """

    response = index.query(
        vector = query_embedding,
        top_k = top_k,
        namespace= PINECONE_NAMESPACE,
        include_metadata=True,
        include_values=False
    )

    return response



def extract_chunks(response):
    """
    Convert Pinecone matches into a simple
    application-friendly structure.
    """

    chunks = []

    for match in response.matches:

        metadata = match.metadata or {}

        chunks.append(
            {
                "id": match.id,
                "score": match.score,
                "text": metadata.get("text", ""),
                "chunk_index": metadata.get(
                    "chunk_index"
                ),
                "company_id": metadata.get(
                    "company_id"
                ),
            }
        )

    return chunks