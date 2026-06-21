# generator.py
import os
from groq import Groq
import config

def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved document chunks using Groq.
    """
    # Initialize Groq client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        return "Error: GROQ_API_KEY is not set or is still using placeholder text in your .env file."
        
    client = Groq(api_key=api_key)

    # Handle the case where the vector DB returned no relevant chunks
    if not retrieved_chunks:
        return "I do not have enough information in the provided student guides to answer that."

    # Format retrieved chunks into a clean context block
    context_blocks = []
    for idx, chunk in enumerate(retrieved_chunks, 1):
        context_blocks.append(f"--- Document Source: {chunk['game']} ---\n{chunk['text']}")
    
    context_str = "\n\n".join(context_blocks)

    # Build an ultra-strict, hallucination-resistant system prompt
    system_prompt = (
        "You are 'The Unofficial Guide' AI assistant for college students. Your sole task is to answer user queries using ONLY the provided student context documents.\n\n"
        "STRICT GROUNDING RULES:\n"
        "1. Answer the query relying EXCLUSIVELY on the facts stated in the context text below. Do NOT use outside general knowledge.\n"
        "2. For every fact or piece of advice you share, explicitly cite the source document inline using brackets (e.g., [reddit_cs3358] or [rmp_koh_assembly]).\n"
        "3. If the context does not contain direct answers to the query, respond EXACTLY with: 'I do not have enough information on that in the current unofficial guides.' Do not guess, summarize general advice, or hallucinate.\n\n"
        f"CONTEXT AVAILABLE:\n{context_str}"
    )

    try:
        completion = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.0, # Setting temperature to 0.0 forces maximum determinism
            max_tokens=600
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An exception occurred during generation: {str(e)}"