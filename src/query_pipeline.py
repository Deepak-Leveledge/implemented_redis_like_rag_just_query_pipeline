from src.embedding import (
    generate_query_embedding,
)

from src.exact_cache import (
    get_exact_cache,
    set_exact_cache,
)

from src.semantic_cache import (
    search_semantic_cache,
    set_semantic_cache,
)

from src.rag_pipeline import (
    run_rag_from_embedding,
)


def query_pipeline(
    question: str,
    top_k: int = 5,
):
    """
    Complete RAG query pipeline:

    1. Exact cache
    2. Query embedding
    3. Semantic cache
    4. Pinecone
    5. Context assembly
    6. Gemini LLM
    7. Cache response
    """

    print("\n")
    print("=" * 70)
    print("START QUERY PIPELINE")
    print("=" * 70)

    print(
        "\nUser Query:",
        question
    )


    # ==================================================
    # STEP 1 — EXACT CACHE
    # ==================================================

    exact_result = get_exact_cache(
        question
    )


    if exact_result is not None:

        print(
            "\nReturning from EXACT CACHE."
        )

        return {
            "answer": exact_result["response"],
            "sources": exact_result["sources"],
            "cache_type": "exact",
        }


    # ==================================================
    # STEP 2 — QUERY EMBEDDING
    # ==================================================

    print(
        "\nGenerating Gemini query embedding..."
    )

    query_embedding = (
        generate_query_embedding(
            question
        )
    )


    print(
        "Embedding dimension:",
        len(query_embedding)
    )


    # ==================================================
    # STEP 3 — SEMANTIC CACHE
    # ==================================================

    semantic_result = search_semantic_cache(
        query_embedding
    )


    if semantic_result is not None:

        print(
            "\nReturning from SEMANTIC CACHE."
        )


        # ----------------------------------------------
        # Promote this query into exact cache
        # ----------------------------------------------

        set_exact_cache(

            query=question,

            response=semantic_result[
                "response"
            ],

            sources=semantic_result[
                "sources"
            ],
        )


        return {
            "answer": semantic_result[
                "response"
            ],
            "sources": semantic_result[
                "sources"
            ],
            "cache_type": "semantic",
            "semantic_distance": semantic_result[
                "distance"
            ],
        }


    # ==================================================
    # STEP 4–6 — REAL RAG
    # ==================================================

    print(
        "\nRunning REAL RAG pipeline..."
    )


    rag_result = run_rag_from_embedding(

        question=question,

        query_embedding=query_embedding,

        top_k=top_k,
    )


    answer = rag_result[
        "answer"
    ]

    sources = rag_result[
        "sources"
    ]


    # ==================================================
    # STEP 7 — EXACT CACHE
    # ==================================================

    set_exact_cache(

        query=question,

        response=answer,

        sources=sources,
    )


    # ==================================================
    # STEP 8 — SEMANTIC CACHE
    # ==================================================

    set_semantic_cache(

        prompt=question,

        response=answer,

        embedding=query_embedding,

        sources=sources,
    )


    print(
        "\nResponse cached in:"
    )

    print(
        "1. Exact Redis Cache"
    )

    print(
        "2. Semantic Redis Cache"
    )


    return {
        "answer": answer,
        "sources": sources,
        "cache_type": "generated",
    }