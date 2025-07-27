# Multi-Level Large Code Summarizer
Suddenly seeing a large code repositories and being told to work with it is a daunting experience. Without any knowledge of the purpose of the repository as a whole, it is difficult to work on any new task. Hence, in this project we worked on multi-level large code summarizer that works on 3 abstraction levels - function, file and repository - to generate a coherent and layered understanding of large scale software systems. 

## Table of Content
- [Overview](#multi-level-large-code-summarizer)
- [Installation](#installation)
- [Methodology](#methodology)
- [Results](#results)
- [Demo](#demo)
- [Run in Colab](#run-in-colab)
- [References]
## Installation
1. Clone the repo
```bash
git clone https://github.com/aarushi211/Multi-Level-Code-Summarization.git
cd multi-level-code-summarizer
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. For Evaluation run app.py and to get prediction use gradio_app.py
```bash
python app.py
```

## Methodology
We used the CodeSearchNet dataset (https://github.com/github/CodeSearchNet). Since it is a large dataset, so due to resource restrictions, we have used only 1% of training data.
* We filtered out the valid function-summary pairs.
* Next we created a nested dictionary:
    * First level key: repository_name
    * Second level key: func_path_in_repository (i.e., file path)
    * Values: List of function code strings in that file
* **Function Level Summary:** 
    * We used `Salesforce/codet5-base-multi-sum` (https://huggingface.co/Salesforce/codet5-base-multi-sum) to directly summarize the functions. 
    * Evaluate using ROUGE and BertScore Similarity.
* **File Level Summary:**
    * Use AST to extract all functions.
    * Summarize and map each function summary with function name.
    * Filter top k longest functions.
    * Build a graph to determine the function and method structure and calls.
    * Combine top function summaries with graph structure into a prompt.
    * Summarize file using `allenai/led-base-16384` (https://huggingface.co/allenai/led-base-16384).
    * Evaluate using BertScore and Cosine Similarity.
* **Repository Level Summary:**
    * Collect the file content from the repository and store the content in dictonary using file path and code of file.
    * Similar to file level, create a graph based context.
    * Summarize file using `allenai/led-base-16384` (https://huggingface.co/allenai/led-base-16384).
    * Evaluate using BertScore and Cosine Similarity. 

## Results
**Function Level**
* rouge1: 43.76
* rouge2: 36.68
* rougeL: 42.44
* rougeLsum: 43.46
* BERTScore: 85.76

**File Level**
* File BERTScore: 77.14
* Cosine Similarity: 55.79

**Repository Level**
* BERTScore: 77.11
* Cosine Similarity: 52.71

## Demo
A demo is available at - https://huggingface.co/spaces/aarushi-211/Multi-Level-Code-Summarizer

## Run in Colab
The below example implements 1% of dataset on the evaluation metrics.

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z4xXoZIthh28OXF2p95zYhcyXWXwXQ_-?usp=sharing)

## References
- CodeT5: [Wang et al., EMNLP 2021](https://arxiv.org/abs/2109.00859)
- Longformer/LED: [Beltagy et al., 2020](https://arxiv.org/abs/2004.05150)
- CodeSearchNet: [Husain et al., 2019](https://arxiv.org/abs/1909.09436)