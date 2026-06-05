# RHELM: Beyond Static Dialogues

**Beyond Static Dialogues: Benchmarking Realistic, Heterogeneous, and Evolving Long-Horizon Memory**

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org/pdf/2605.31086)
[![Project Page](https://img.shields.io/badge/Project-Page-blue)](https://microsoft.github.io/RHELM/)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Dataset-yellow)](https://huggingface.co/datasets/microsoft/RHELM)
[![GitHub](https://img.shields.io/badge/Code-GitHub-black)](https://github.com/microsoft/RHELM)
<!-- [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) -->

<p align="center">
  <img src="assets/main.png" alt="RHELM Overview" width="100%">
</p>

## 📖 Overview

RHELM is a comprehensive benchmark for evaluating long-horizon memory capabilities in AI systems. Unlike existing benchmarks that focus on static dialogues, RHELM introduces **realistic**, **heterogeneous**, and **evolving** memory challenges that better reflect real-world assistant scenarios.

### Key Features

- 🎭 **Realistic Profiles**: Diverse characters with rich backstories, preferences, and evolving life circumstances
- 📊 **Heterogeneous Data**: Multi-modal external memory sources including conversations, emails, documents
- 🔄 **Temporal Evolution**: Time-aware questions that test memory across different temporal contexts
- 🧠 **Challenging Question Taxonomy**: 7 major categories with 26 complex characteristics requiring multi-hop reasoning, temporal synthesis, preference tracking, and hallucination detection
- ⚠️ **Memory-Conditioned Misleading Queries**: "Trap" queries that conflict with the user's updated life state, requiring the assistant to detect the implicit conflict, decline the unsafe request, and propose a constraint-compliant alternative
<!-- - 🎯 **Advanced Reasoning Requirements**: Questions designed to test entity disambiguation, causal reasoning, anomaly detection, and cross-document inference -->

## 📋 Challenge Taxonomy

RHELM features a comprehensive taxonomy of challenging memory questions across three major QA domains with **7 categories** and **26 complex characteristics**.

👉 **[View Full Challenge Taxonomy](docs/CHALLENGE_TAXONOMY.md)**


## 🏆 Leaderboard

We evaluate three families of systems — **RAG Baselines**, **Long-Context Models**, and **Memory Frameworks** — under two settings (**without** / **with** external data sources). Scores are accuracy (%), reported across **Dialogue History QA** (`FC`: Fact, `TP`: Temporal, `AG`: Aggregation, `HL`: Hallucination, `MI`: Misleading), **External Source QA** (`EX`: Attachment & Email), and **Hybrid Context QA** (`MX`: Mixed).

### 🟢 Without External Data Sources

| Model | FC | TP | AG | HL | MI | EX | MX | **Avg** |
|:------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| *RAG Baselines* | | | | | | | | |
| GPT-4.1-mini *(k=5)* | 35.8 | 17.3 | 17.7 | 15.2 | 3.1 | 8.0 | 10.0 | 16.3 |
| GPT-4.1-mini *(k=20)* | 44.0 | 32.4 | 31.8 | 18.3 | 3.1 | 12.1 | 12.9 | 23.5 |
| GPT-4.1-mini *(k=50)* | 59.9 | 41.6 | 40.1 | 15.7 | 1.5 | 12.9 | 16.7 | 28.9 |
| Hybrid *(k=5)* | 34.3 | 20.5 | 14.1 | 19.8 | 1.5 | 8.0 | 10.5 | 16.7 |
| Hybrid *(k=20)* | 47.3 | 35.7 | 31.8 | 19.3 | 3.1 | 10.4 | 15.2 | 24.8 |
| Hybrid *(k=50)* | 56.5 | 41.1 | 35.9 | 15.2 | 3.1 | 13.7 | 16.7 | 27.8 |
| GPT-4.1 *(k=20)* | 51.7 | 34.1 | 35.9 | 23.9 | 7.7 | <u>16.1</u> | 17.6 | 28.2 |
| Gemini-2.5-Pro *(k=20)* | 45.4 | 35.1 | 27.1 | 66.0 | 23.1 | 12.4 | 18.1 | 32.6 |
| Claude-Opus-4.5 *(k=20)* | 50.7 | 37.8 | 33.3 | 68.0 | <u>47.7</u> | 13.7 | 16.2 | 36.2 |
| *Long-Context Models* | | | | | | | | |
| Gemini-2.5-Flash-Lite *(1M)* | 33.2 | 22.7 | 15.2 | 17.3 | 0.0 | 9.5 | 5.6 | 16.0 |
| Qwen-2.5-14B-Instruct *(1M)* | 29.5 | 15.1 | 29.7 | 3.1 | 0.0 | 11.7 | 9.1 | 15.3 |
| GPT-4.1-mini *(1M)* | 55.1 | 31.9 | 40.1 | 4.1 | 1.5 | 11.2 | 12.4 | 24.0 |
| Qwen3.5-397B-A17B *(1M)* | 49.8 | 33.0 | 35.9 | <u>73.6</u> | 23.1 | 10.8 | 14.8 | 34.6 |
| Claude-Opus-4.6 *(1M)* | <u>72.5</u> | <u>67.6</u> | <u>58.3</u> | 67.0 | **69.2** | <u>16.1</u> | <u>21.4</u> | <u>49.7</u> |
| GPT-5.5 *(1M)* | **82.6** | **83.8** | **65.1** | **77.7** | 26.2 | **24.9** | **29.1** | **57.0** |
| *Memory Frameworks* | | | | | | | | |
| [MemGPT](https://github.com/cpacker/MemGPT) | 31.9 | 18.4 | 22.9 | 0.5 | 0.0 | 7.6 | 8.1 | 13.9 |
| [Mem0](https://github.com/mem0ai/mem0) | 41.6 | 31.4 | 28.1 | 10.7 | 3.1 | 10.8 | 13.3 | 21.1 |
| [MemU](https://github.com/NevaMind-AI/memU) | 49.3 | 32.4 | 33.9 | 8.6 | 4.6 | 12.0 | 11.4 | 23.1 |

### 🔵 With External Data Sources

| Model | FC | TP | AG | HL | MI | EX | MX | **Avg** |
|:------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| *RAG Baselines* | | | | | | | | |
| GPT-4.1-mini *(k=5)* | 34.8 | 14.1 | 19.3 | 11.7 | 3.1 | 16.9 | 12.4 | 17.5 |
| GPT-4.1-mini *(k=20)* | 42.5 | 28.7 | 30.7 | 13.2 | 3.1 | 28.5 | 13.8 | 25.1 |
| GPT-4.1-mini *(k=50)* | 54.6 | 39.5 | <u>38.0</u> | 11.2 | 1.5 | 38.6 | 22.4 | 32.6 |
| Hybrid *(k=5)* | 31.9 | 19.5 | 14.1 | 19.3 | 1.5 | 16.1 | 10.5 | 17.6 |
| Hybrid *(k=20)* | 45.9 | 30.8 | 26.6 | 16.8 | 4.6 | 26.9 | 15.7 | 26.0 |
| Hybrid *(k=50)* | 53.1 | 37.8 | 33.9 | 8.6 | 3.1 | 33.3 | 18.6 | 29.6 |
| GPT-4.1 *(k=20)* | 50.2 | 29.2 | 32.3 | 19.8 | 6.2 | 32.5 | 19.5 | 29.5 |
| Gemini-2.5-Pro *(k=20)* | 43.0 | 31.9 | 26.0 | 64.5 | 26.2 | 31.3 | 20.5 | 35.5 |
| Claude-Opus-4.5 *(k=20)* | 50.2 | 30.8 | 31.8 | 60.9 | <u>41.5</u> | 33.7 | 21.0 | 38.1 |
| *Long-Context Models* | | | | | | | | |
| Gemini-2.5-Flash-Lite *(1M)* | 31.7 | 14.1 | 23.4 | 7.6 | 0.0 | 19.0 | 13.1 | 17.3 |
| Qwen-2.5-14B-Instruct *(1M)* | 16.9 | 7.0 | 15.6 | 1.0 | 0.0 | 5.2 | 6.2 | 8.1 |
| GPT-4.1-mini *(1M)* | 49.3 | 27.0 | 33.9 | 2.0 | 1.5 | 43.4 | 0.3 | 33.9 |
| Qwen3.5-397B-A17B *(1M)* | 50.2 | 28.7 | 37.0 | 58.9 | 24.6 | 48.2 | 46.7 | 44.3 |
| Claude-Opus-4.6 *(1M)* | <u>68.1</u> | <u>64.3</u> | **56.8** | <u>71.1</u> | **67.7** | <u>74.7</u> | <u>77.6</u> | <u>69.1</u> |
| GPT-5.5 *(1M)* | **76.8** | **73.0** | **56.8** | **75.6** | 29.2 | **81.5** | **86.7** | **73.3** |
| *Memory Frameworks* | | | | | | | | |
| [MemGPT](https://github.com/cpacker/MemGPT) | 27.5 | 14.6 | 28.7 | 1.5 | 1.5 | 18.9 | 17.1 | 17.3 |
| [Mem0](https://github.com/mem0ai/mem0) | 46.4 | 29.2 | 27.1 | 10.2 | 3.1 | 31.3 | 35.7 | 28.9 |
| [MemU](https://github.com/NevaMind-AI/memU) | 54.6 | 36.2 | 35.4 | 10.2 | 3.1 | 36.5 | 36.7 | 33.6 |

> 💡 **Notes**: All long-context models are evaluated with a `batch_size` of 10 for inference cost. The relatively low scores of **Qwen3.5-397B-A17B** are mainly caused by JSON parsing failures during evaluation, which suppress its effective accuracy.



## 🗂️ QA Format

Each QA file is in
JSONL format

```json
{
  "id": "fact_19130b",
  "question": "Reflecting on the morning when my routine felt particularly unsettled and I ended up with a less-than-ideal start, what did I actually have for my first meal of the day?",
  "answer": "Leftover lentil soup",
  "question_date": "2024-10-28",
  "question_type": "fact",
  "supporting_evidence": ["2024-05-26:5"],
  "characteristics": ["State-Dependent Attribute"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique question identifier, prefixed by its question type (e.g. `fact_19130b`). |
| `question` | string | The user query posed to the memory system. |
| `answer` | string | The ground-truth answer used for evaluation. |
| `question_date` | string (`YYYY-MM-DD`) | The date from which the question is asked. To better utilize the benchmark complexity, it is recommended to use all history evidence.|
| `question_type` | string | One of: `fact`, `temporal`, `hallucination`, `aggregation`, `misleading`, `attachment`, `mixed`. |
| `supporting_evidence` | list[string] | References to source items that ground the answer. Conversation evidence uses the form `"<session-date>:<turn-index>"` (e.g. `"2024-05-26:5"` = turn 5 of the 2024-05-26 session); attachment evidence references the file/section (e.g. `"56_report_task_*.md:Section"`). |
| `characteristics` | list[string] | Fine-grained challenge labels for the question (e.g. `State-Dependent Attribute`, `Multi-Hop Traversal`). See the [Challenge Taxonomy](docs/CHALLENGE_TAXONOMY.md). |


## 🚀 Quick Start

### Installation

```bash

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Evaluation

The evaluation reads its dataset from the `data/` directory (conversations, emails,
attachments) and a QA file in JSONL format. Provide the QA file via `--input-file`:

```bash
# Basic RAG evaluation (dense retrieval, top-k=5)
python -m evaluation.rag_benchmark \
    --character "David_R._Ellis" \
    --input-file "data/QA_final/low_score_qa_David_R._Ellis_all_validated.jsonl"

# Full-context evaluation (no retrieval, feed all evidence to the model)
python -m evaluation.rag_benchmark \
    --character "David_R._Ellis" \
    --input-file "data/QA_final/low_score_qa_David_R._Ellis_all_validated.jsonl" \
    --full-context

# RAG evaluation including emails and attachments, with hybrid (BM25 + dense) retrieval
python -m evaluation.rag_benchmark \
    --character "David_R._Ellis" \
    --input-file "data/QA_final/low_score_qa_David_R._Ellis_all_validated.jsonl" \
    --include-attachment \
    --hybrid \
    --k 10
```

### Configuration

LLM credentials are read from environment variables (never hard-coded):

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# or Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_API_KEY="..."
```

Dataset locations, embedding model, chunking and output paths can be customised in
[evaluation/configs/config.py](evaluation/configs/config.py).

## 📦 Data & Code Release

| Component | Status |
|-----------|--------|
| Evaluation Framework | ✅ Available |
| Benchmark Data | [🤗 HuggingFace](https://github.com/microsoft/RHELM) |
| Data Generation Code | 🔜 To be released |


---

**Note**: Data generation pipeline will be released upon paper acceptance