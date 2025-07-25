# gradio_demo.py
import gradio as gr
import tempfile
import zipfile
import os
from summarizers.file_summarizers import summarize_file_with_graph
from summarizers.repo_summarizers import summarize_repo_with_graph
from models.models import func_summarizer

# ------------------------------------------------------------------
# 1. Function-level tab
# ------------------------------------------------------------------
def summarize_function(code: str) -> str:
    if not code.strip():
        return "⚠️ Please paste some code."
    out = func_summarizer(code, max_length=64, do_sample=False, truncation=True)
    return out[0]["generated_text"].strip()

# ------------------------------------------------------------------
# 2. File-level tab
# ------------------------------------------------------------------
def summarize_file(file_path) -> str:
    if file_path is None:
        return "⚠️ No file uploaded."
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    return summarize_file_with_graph(code, top_k=5)

# ------------------------------------------------------------------
# 3. Repository-level tab
# ------------------------------------------------------------------
def summarize_repo(file_list):
    file_contents = {}

    for file_or_zip in file_list:
        path = file_or_zip.name
        # Case 1: single .py file
        if path.endswith(".py"):
            with open(path, "r", encoding="utf-8") as fh:
                file_contents[os.path.basename(path)] = fh.read()

        # Case 2: ZIP archive
        elif path.endswith(".zip"):
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(path, "r") as zf:
                    zf.extractall(tmpdir)
                for root, _, files in os.walk(tmpdir):
                    for f in files:
                        if f.endswith(".py"):
                            abs_path = os.path.join(root, f)
                            rel_path = os.path.relpath(abs_path, tmpdir)
                            with open(abs_path, "r", encoding="utf-8") as fh:
                                file_contents[rel_path] = fh.read()

    if not file_contents:
        return "⚠️ No Python files found."

    return summarize_repo_with_graph(file_contents, top_files=5, top_k_funcs=5)

# ------------------------------------------------------------------
# Gradio UI
# ------------------------------------------------------------------
with gr.Blocks(title="Large-Code-Summarizer") as demo:
    gr.Markdown("# 🧠 Large-Code-Summarizer\nGenerate summaries at **function**, **file**, or **repository** level.")

    with gr.Tab("Function"):
        func_code = gr.Code(language="python", label="Paste a Python function")
        func_out  = gr.Textbox(label="Summary", lines=2, interactive=False)
        func_btn  = gr.Button("Summarize")
        func_btn.click(summarize_function, inputs=func_code, outputs=func_out)

    with gr.Tab("File"):
        file_in  = gr.File(file_types=[".py"], label="Upload .py file")
        file_out = gr.Textbox(label="Summary", lines=8, interactive=False)
        file_btn = gr.Button("Summarize")
        file_btn.click(summarize_file, inputs=file_in, outputs=file_out)

    with gr.Tab("Repository"):
        repo_in  = gr.File(file_count="multiple", file_types=[".py", ".zip"], label="Upload .py files or zip")
        repo_out = gr.Textbox(label="Summary", lines=10, interactive=False)
        repo_btn = gr.Button("Summarize")
        repo_btn.click(summarize_repo, inputs=repo_in, outputs=repo_out)

# Launch
if __name__ == "__main__":
    demo.launch(share=False) 