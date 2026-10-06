# ##Testing the ALL Configuration in the from the env

# from src.config import (
#     EMBEDDING_MODEL,
#     EMBEDDING_DIMENSION,
#     LLM_MODEL,
#     PINECONE_INDEX_NAME,
#     PINECONE_NAMESPACE,
#     REDIS_URL,
# )


# print("Embedding Model :", EMBEDDING_MODEL)
# print("Embedding Dim   :", EMBEDDING_DIMENSION)
# print("LLM Model       :", LLM_MODEL)
# print("Pinecone Index  :", PINECONE_INDEX_NAME)
# print("Namespace       :", PINECONE_NAMESPACE)
# print("Redis URL       :", REDIS_URL)


# # Reside connection testing 
# from src.redis_client import test_redis_connection , redis_client


# if test_redis_connection():
#     print("Redis Connection is Establish")
# else:
#     print("Redis Connection Error")


# redis_client.set(
#     "rag:testing",
#     "Redis is working"
# )

# values = redis_client.get(
#     "rag:testing"
# )

# print(f"Redis First Key Name is {values}")



# #testing exact cache code which is exact_cache.py

# from src.exact_cache import (get_exact_cache,set_exact_cache)



# query = "What is the leave policy?"


# # --------------------------------
# # 1. Check cache
# # --------------------------------

# cached_result = get_exact_cache(query)


# if cached_result:

#     print("\nReturning cached response:")
#     print(cached_result["response"])

# else:

#     # --------------------------------
#     # Simulating RAG/LLM response
#     # --------------------------------

#     generated_response = (
#         "Employees are entitled to paid leave "
#         "according to the company HR policy."
#     )

#     sources = [
#         {
#             "document": "HR Policy",
#             "page": 1
#         }
#     ]

#     # --------------------------------
#     # Store in Redis
#     # --------------------------------

#     cache_key = set_exact_cache(
#         query=query,
#         response=generated_response,
#         sources=sources,
#     )

#     print("\nGenerated response:")
#     print(generated_response)

#     print("\nRedis key:")
#     print(cache_key)


########################################
#emedding test
########################################

# from src.embedding import generate_query_embedding


# query = "What is the leave policy?"


# embedding = generate_query_embedding(query)


# print("Query:")
# print(query)

# print("\nEmbedding Length:")
# print(len(embedding))

# print("\nFirst 10 values:")
# print(embedding[:10])


# # Check vector norm
# import numpy as np

# norm = np.linalg.norm(
#     np.array(embedding)
# )

# print("\nVector Norm:")
# print(norm)





#######################################################
#Pine conde client testing 
#######################################################


# from src.pinecone_client import (get_index_stats,search_pinecone,extract_chunks)
# from src.embedding import generate_query_embedding



# # -----------------------------
# # 1. Check Pinecone Stats
# # -----------------------------

# stats = get_index_stats()

# print("Pinecone Dimension:", stats.dimension)
# print("Total Vectors:", stats.total_vector_count)

# print("\nNamespaces:")

# for namespace, summary in stats.namespaces.items():
#     print(
#         namespace,
#         "->",
#         summary.vector_count
#     )




# # -----------------------------
# # 2. Create Query Embedding
# # -----------------------------

# query = "What is the leave policy?"

# embedding = generate_query_embedding(
#     query
# )


# print("\nQuery:", query)
# print("Embedding Dimension:", len(embedding))


# # -----------------------------
# # 3. Search Pinecone
# # -----------------------------

# results = search_pinecone(
#     query_embedding=embedding,
#     top_k=5,
# )


# chunks = extract_chunks(
#     results
# )

# print("\nClean Chunks:")
# print("=" * 60)

# for chunk in chunks:

#     print("\nID:", chunk["id"])
#     print("Score:", chunk["score"])
#     print("Chunk Index:", chunk["chunk_index"])
#     print("Company:", chunk["company_id"])
#     print("Text:", chunk["text"][:500])




# print("\nRaw Pinecone Response:")
# print(results)

# print("\nNamespace returned:")
# print(results.namespace)

# print("\nNumber of matches:")
# print(len(results.matches))

# print("\nMatches object:")
# print(results.matches)

# # -----------------------------
# # 4. Print Results
# # -----------------------------

# print("\nPinecone Results:")
# print("=" * 60)


# for i, match in enumerate(
#     results.matches,
#     start=1
# ):

#     print(f"\nResult #{i}")

#     print("ID:")
#     print(match.id)

#     print("\nScore:")
#     print(match.score)

#     print("\nMetadata:")
#     print(match.metadata)

#     print("-" * 60)




####################################################
# sematic cache crete index testing
####################################################




# from src.semantic_cache import (
#     create_semantic_index,
# )


# create_semantic_index()


# from src.semantic_cache import (
#     create_semantic_index,
#     set_semantic_cache,
#     search_semantic_cache,
# )

# from src.embedding import (
#     generate_query_embedding,
# )


# # =========================================================
# # 1. Create Redis Semantic Index
# # =========================================================

# create_semantic_index()


# # =========================================================
# # 2. Canonical Question
# # =========================================================

# original_query = (
#     "How many leaves can employees take?"
# )


# # =========================================================
# # 3. Generate Embedding
# # =========================================================

# original_embedding = (
#     generate_query_embedding(
#         original_query
#     )
# )


# # =========================================================
# # 4. Store Fake Cached Response
# # =========================================================

# set_semantic_cache(

#     prompt=original_query,

#     response=(
#         "Employees are entitled to "
#         "paid leave according to the "
#         "company HR policy."
#     ),

#     embedding=original_embedding,

#     sources=[
#         {
#             "document": "HR Policy",
#             "page": 1
#         }
#     ],
# )


# # =========================================================
# # 5. New Query
# # =========================================================

# new_query = (
#     "How many leaves can employees take?"
# )


# new_embedding = (
#     generate_query_embedding(
#         new_query
#     )
# )


# # =========================================================
# # 6. Semantic Search
# # =========================================================

# result = search_semantic_cache(
#     new_embedding
# )


# # =========================================================
# # 7. Print Result
# # =========================================================

# print(
#     "\nFinal Result:"
# )

# print(result)





# rag resting LLm + pinecone 

# from src.rag_pipeline import (
#     run_rag_without_cache,
# )


# question = (
#     "What is the checkout and check in timing?"
# )


# result = run_rag_without_cache(
#     question=question,
#     top_k=5,
# )


# print("\n")
# print("=" * 70)
# print("FINAL ANSWER")
# print("=" * 70)

# print(
#     result["answer"]
# )


# print("\n")
# print("=" * 70)
# print("SOURCES")
# print("=" * 70)


# for chunk in result["chunks"]:

#     print(
#         f"\nID: {chunk['id']}"
#     )

#     print(
#         f"Score: {chunk['score']}"
#     )

#     print(
#         f"Chunk Index: {chunk['chunk_index']}"
#     )

from src.metric import print_metrics

from src.query_pipeline import (
    query_pipeline,
)


question = (
    "other then villa there is other place to chill and enjoy"
)


result = query_pipeline(
    question=question,
    top_k=5,
)


print("\n")
print("=" * 70)
print("FINAL RESULT")
print("=" * 70)


print(
    "\nAnswer:"
)

print(
    result["answer"]
)


print(
    "\nCache Type:"
)

print(
    result["cache_type"]
)


if "semantic_distance" in result:

    print(
        "\nSemantic Distance:"
    )

    print(
        result["semantic_distance"]
    )


print(
    "\nSources:"
)

for source in result["sources"]:

    print(
        source
    )

print_metrics()