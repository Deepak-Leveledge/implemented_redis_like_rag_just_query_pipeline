from src.embedding import (
    generate_query_embedding,
)

from src.pinecone_client import (
    search_pinecone,
    extract_chunks,
)

from src.llm import (
    generate_rag_response,
)


def build_context(
    chunks: list[dict],
) -> str:
    """
    Convert retrieved Pinecone chunks
    into the context sent to the LLM.
    """

    context_parts = []

    for i, chunk in enumerate(
        chunks,
        start=1,
    ):

        text = chunk.get(
            "text",
            ""
        ).strip()

        if not text:
            continue

        context_parts.append(
            f"""
--- Context Chunk {i} ---

Source ID:
{chunk.get("id")}

Relevance Score:
{chunk.get("score")}

{text}
"""
        )

    if not context_parts:
        return (
            "No relevant context was found."
        )

    return "\n".join(
        context_parts
    )


def build_sources(
    chunks: list[dict],
) -> list[dict]:
    """
    Keep only useful source information
    for caching and response display.
    """

    sources = []

    for chunk in chunks:

        sources.append(
            {
                "id": chunk.get("id"),
                "score": chunk.get("score"),
                "chunk_index": chunk.get(
                    "chunk_index"
                ),
                "company_id": chunk.get(
                    "company_id"
                ),
            }
        )

    return sources


def run_rag_from_embedding(
    question: str,
    query_embedding: list[float],
    top_k: int = 5,
):
    """
    Run Pinecone retrieval + context assembly
    + Gemini LLM using an already generated embedding.

    The embedding is NOT generated again.
    """

    # ---------------------------------
    # 1. Pinecone Search
    # ---------------------------------

    pinecone_results = search_pinecone(
        query_embedding=query_embedding,
        top_k=top_k,
    )


    # ---------------------------------
    # 2. Extract Chunks
    # ---------------------------------

    chunks = extract_chunks(
        pinecone_results
    )


    print(
        "\nRetrieved chunks:",
        len(chunks)
    )


    # ---------------------------------
    # 3. Context Assembly
    # ---------------------------------

    context = build_context(
        chunks
    )


    print(
        "Context assembled."
    )


    # ---------------------------------
    # 4. Gemini LLM
    # ---------------------------------

    answer = generate_rag_response(
        question=question,
        context=context,
    )


    # ---------------------------------
    # 5. Sources
    # ---------------------------------

    sources = build_sources(
        chunks
    )


    return {
        "question": question,
        "answer": answer,
        "chunks": chunks,
        "context": context,
        "sources": sources,
        "query_embedding": query_embedding,
    }


def run_rag_without_cache(
    question: str,
    top_k: int = 5,
):
    """
    Complete RAG without Redis cache.

    Kept for independent testing.
    """

    query_embedding = (
        generate_query_embedding(
            question
        )
    )

    return run_rag_from_embedding(
        question=question,
        query_embedding=query_embedding,
        top_k=top_k,
    )