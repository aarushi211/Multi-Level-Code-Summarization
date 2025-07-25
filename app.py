from datasets import load_dataset
from collections import defaultdict
from evaluators.evaluators import evaluate_function_level, evaluate_unsupervised_level
from summarizers.file_summarizers import summarize_file_with_graph
from summarizers.repo_summarizers import summarize_repo_with_graph
from models.models import func_summarizer
import os, shutil

# Load and group data
# dataset = load_dataset("code_search_net", "python", split="train[:1%]")


def safe_load_code_search_net(split="train[:1%]", cache_dir=None):
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/huggingface/datasets/code_search_net")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    return load_dataset("code_search_net", "python", split=split)

dataset = safe_load_code_search_net()
dataset = dataset.filter(lambda x: x["func_code_string"] and x["func_documentation_string"])

# Group repo → file → code
repo_map = defaultdict(lambda: defaultdict(list))
for item in dataset:
    repo_map[item["repository_name"]][item["func_path_in_repository"]].append(item["func_code_string"])

# ========== FUNCTION-LEVEL (First 100 functions) ==========

print("\n================ FUNCTION LEVEL EVALUATION ================\n")

func_codes = [item["func_code_string"] for item in dataset.select(range(100))]
func_refs = [item["func_documentation_string"] for item in dataset.select(range(100))]
func_preds = [out["generated_text"].strip() for out in func_summarizer(func_codes, max_length=64, do_sample=False)]

evaluate_function_level(func_preds, func_refs)

# ========== FILE-LEVEL (Top 3 repos × 3 files each) ==========

print("\n================ FILE LEVEL EVALUATION ================\n")

file_bert_scores = []
file_cos_scores = []

for repo_name in list(repo_map.keys())[:3]:
    for file_path, func_list in list(repo_map[repo_name].items())[:3]:
        raw_code = "\n".join(func_list)
        try:
            file_summary = summarize_file_with_graph(raw_code, top_k=5)
            bert, cos = evaluate_unsupervised_level(file_summary, raw_code, label="File")
            file_bert_scores.append(bert)
            file_cos_scores.append(cos)
        except Exception as e:
            print(f"Skipped file {file_path} due to: {e}")

print(f"\nAvg File BERTScore: {sum(file_bert_scores)/len(file_bert_scores):.4f}")
print(f"Avg File Cosine Similarity: {sum(file_cos_scores)/len(file_cos_scores):.4f}")

# ========== REPO-LEVEL (Top 5 repos) ==========

print("\n================ REPO LEVEL EVALUATION ================\n")

repo_bert_scores = []
repo_cos_scores = []

for repo_name in list(repo_map.keys())[:5]:
    file_contents = {
        path: "\n".join(funcs)
        for path, funcs in list(repo_map[repo_name].items())[:5]
    }

    try:
        repo_summary = summarize_repo_with_graph(file_contents, top_files=5, top_k_funcs=5)
        raw_repo_code = "\n".join(file_contents.values())[:5000]
        bert, cos = evaluate_unsupervised_level(repo_summary, raw_repo_code, label="Repo")
        repo_bert_scores.append(bert)
        repo_cos_scores.append(cos)
    except Exception as e:
        print(f"Skipped repo {repo_name} due to: {e}")

print(f"\nAvg Repo BERTScore: {sum(repo_bert_scores)/len(repo_bert_scores):.4f}")
print(f"Avg Repo Cosine Similarity: {sum(repo_cos_scores)/len(repo_cos_scores):.4f}")
