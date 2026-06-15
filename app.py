import gradio as gr
from rag_engine.retriever import retrieve
from rag_engine.agent import generate_response


def handle_query(question, chat_history, api_history):
    chunks = retrieve(question)
    result = generate_response(question, chunks, history=api_history)

    api_history = api_history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": result["answer"]},
    ]
    chat_history = chat_history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": result["answer"]},
    ]
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return "", chat_history, api_history, sources


with gr.Blocks() as demo:
    api_history = gr.State([])

    gr.Markdown("## GMU & DMV Area Guide")
    chatbot = gr.Chatbot(label="Conversation", height=450)
    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="Ask about things to do, food, events…", scale=4)
        btn = gr.Button("Ask", scale=1)
        clear_btn = gr.Button("New Chat", scale=1)
    sources = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    btn.click(handle_query, inputs=[inp, chatbot, api_history], outputs=[inp, chatbot, api_history, sources])
    inp.submit(handle_query, inputs=[inp, chatbot, api_history], outputs=[inp, chatbot, api_history, sources])
    clear_btn.click(lambda: ([], [], ""), outputs=[chatbot, api_history, sources])

demo.launch()