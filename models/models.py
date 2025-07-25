import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer

device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base-multi-sum")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base-multi-sum")

func_summarizer = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
    batch_size=8,
)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

file_summarizer = pipeline(
    "summarization",
    model="allenai/led-base-16384",
    tokenizer="allenai/led-base-16384",
    device=device,
    truncation=True,
    max_length=128,
    min_length=64,
)