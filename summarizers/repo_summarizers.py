from summarizers.file_summarizers import summarize_file_with_graph
from models.models import file_summarizer

def summarize_repo_with_graph(file_dict: dict, top_files=5, top_k_funcs=5):
    """
    Summarize a repository:
    - Summarize each file using summarize_file_with_graph
    - Combine top-k summaries
    - Feed to LED summarizer
    """
    file_summaries = []

    for file_path, code_text in list(file_dict.items())[:top_files]:
        try:
            summary = summarize_file_with_graph(code_text, top_k=top_k_funcs)
            file_summaries.append(summary)
        except Exception as e:
            print(f"Skipped file {file_path} due to: {e}")

    if not file_summaries:
        return "No valid summaries found."

    combined_input = "\n\n".join(file_summaries)
    final_summary = file_summarizer(
        combined_input,
        max_length=256,
        min_length=100,
        no_repeat_ngram_size=3,
        do_sample=False,
    )[0]["summary_text"]

    return final_summary

# from transformers import AutoTokenizer

# # reuse the same tokenizer instance you already loaded
# tokenizer = file_summarizer.tokenizer

# def summarize_repo_with_graph(file_dict: dict, top_files=5, top_k_funcs=5):
#     file_summaries = []

#     for file_path, code_text in list(file_dict.items())[:top_files]:
#         try:
#             summary = summarize_file_with_graph(code_text, top_k=top_k_funcs)
#             file_summaries.append(summary)
#         except Exception as e:
#             print(f"Skipped file {file_path} due to: {e}")

#     if not file_summaries:
#         return "No valid summaries found."

#     combined_input = "\n\n".join(file_summaries)

#     # dynamic length cap
#     tokens = tokenizer.encode(combined_input, truncation=False)
#     suggested_max = min(256, max(100, len(tokens) // 2))
#     suggested_min = min(100, suggested_max - 20)

#     final_summary = file_summarizer(
#         combined_input,
#         max_length=suggested_max,
#         min_length=suggested_min,
#         no_repeat_ngram_size=3,
#         do_sample=False,
#     )[0]["summary_text"]

#     return final_summary
