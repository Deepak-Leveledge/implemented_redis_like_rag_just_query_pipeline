from google import genai
from src.config import (GEMINI_API_KEY,LLM_MODEL)


# Gemini Client

client = genai.Client(api_key=GEMINI_API_KEY)



def generate_rag_response(
        question:str,
        context:str
) -> str:

    prompt = f"""
You are a helpful company knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not available in the context,
   clearly say that the information was not found
   in the provided company documents.
4. Keep the answer clear and concise.

Context:
--------------------
{context}
--------------------

User Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


