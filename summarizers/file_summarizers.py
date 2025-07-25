from parsers.parsers import extract_functions_from_code, extract_call_graph, extract_class_hierarchy
from graphs.graph_utils import format_graph_context
from models.models import func_summarizer, file_summarizer

def summarize_file_with_graph(code_text: str, top_k: int = 5):
    """
    Summarize a file by:
    - Extracting function-level summaries using CodeT5
    - Building call/class hierarchy (graph_utils)
    - Creating structured prompt for LED summarizer
    """
    functions = extract_functions_from_code(code_text)
    if not functions:
        return "No functions found."

    func_names = list(functions.keys())
    func_bodies = list(functions.values())

    # Summarize functions
    func_summaries_raw = func_summarizer(func_bodies, max_length=64, do_sample=False)
    func_summaries = {
        func_names[i]: func_summaries_raw[i]["generated_text"].strip()
        for i in range(len(func_names))
    }

    # Select top-k longest functions as proxy for importance
    top_funcs = sorted(func_summaries.items(), key=lambda x: len(functions[x[0]]), reverse=True)[:top_k]
    top_func_summaries = {k: v for k, v in top_funcs}

    # Build graph context
    call_graph = extract_call_graph(code_text)
    class_hierarchy = extract_class_hierarchy(code_text)
    input_text = format_graph_context(top_func_summaries, call_graph, class_hierarchy)

    # Summarize with LED
    summary = file_summarizer(
        input_text,
        max_length=128,
        min_length=64,
        no_repeat_ngram_size=3,
        do_sample=False,
    )[0]["summary_text"]

    return summary