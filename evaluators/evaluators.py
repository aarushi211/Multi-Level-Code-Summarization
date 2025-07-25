import evaluate
from sentence_transformers import util
from models.models import embed_model

rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

def cosine_similarity(preds, refs, batch_size=2):
    pred_embeds = embed_model.encode(preds, convert_to_tensor=True, batch_size=batch_size)
    ref_embeds = embed_model.encode(refs, convert_to_tensor=True, batch_size=batch_size)
    return util.cos_sim(pred_embeds, ref_embeds).diag().mean().item()

# ---------------- FUNCTION LEVEL ---------------- #
def evaluate_function_level(preds: list, refs: list):
    rouge_scores = rouge.compute(predictions=preds, references=refs)
    bert = bertscore.compute(predictions=preds, references=refs, lang="en")
    bert_f1 = sum(bert["f1"]) / len(bert["f1"])

    print("\nFunction-Level ROUGE:")
    for metric in ["rouge1", "rouge2", "rougeL", "rougeLsum"]:
        print(f"{metric}: {rouge_scores[metric]:.4f}")
    
    print(f"Function-Level BERTScore: {bert_f1:.4f}")
    return rouge_scores, bert_f1

# ---------------- FILE/REPO LEVEL ---------------- #
def evaluate_unsupervised_level(pred: str, ref: str, label: str = "Repo"):
    bert = bertscore.compute(predictions=[pred], references=[ref], lang="en")["f1"][0]
    cos = cosine_similarity([pred], [ref])

    print(f"\n{label}-Level Evaluation:")
    print(f"BERTScore: {bert:.4f}")
    print(f"Cosine Similarity: {cos:.4f}")

    return bert, cos