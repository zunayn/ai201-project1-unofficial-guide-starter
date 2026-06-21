# app.py
import gradio as gr
import os
from dotenv import load_dotenv
from retriever import retrieve
from generator import generate_response

# Load environment variables
load_dotenv()

def ask(question):
    """Core RAG pipeline function."""
    # Retrieve relevant chunks from ChromaDB
    chunks = retrieve(question)
    
    # Extract a unique list of sources from the retrieved metadata
    unique_sources = []
    if chunks:
        # Use a set to prevent duplicate source names
        unique_sources = list(set(chunk["game"] for chunk in chunks))
    
    # Generate the grounded response
    answer = generate_response(question, chunks)
    
    return {
        "answer": answer,
        "sources": unique_sources
    }

def handle_query(question):
    """Wrapper function for the Gradio UI."""
    if not question.strip():
        return "Please enter a question.", ""
        
    result = ask(question)
    
    # Format the sources list with bullet points
    if result["sources"]:
        sources_formatted = "\n".join(f"• {s}.txt" for s in result["sources"])
    else:
        sources_formatted = "No sources retrieved."
        
    return result["answer"], sources_formatted

#  Build the Gradio UI 
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 The Unofficial Guide: TXST CS & Engineering")
    gr.Markdown("Ask a question about TXST courses, professors, or campus life. Answers are grounded *strictly* in real student reviews and discussions.")
    
    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="e.g., Who should I take for Data Structures (CS 3358)?")
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Grounded Answer", lines=6, interactive=False)
    with gr.Row():
        sources = gr.Textbox(label="Retrieved From", lines=3, interactive=False)
        
    # Bind the button and the Enter key to the handle_query function
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_key_here":
        print("CRITICAL ERROR: Set your GROQ_API_KEY in your .env file before running!")
    else:
        print("Launching Gradio interface... Check your browser!")
        demo.launch()