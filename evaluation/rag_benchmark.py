#!/usr/bin/env python3
"""
RAG Benchmark System for Memory Evaluation

This module implements a benchmark system that:
1. Loads QA pairs from a JSONL file
2. Uses the RAG system to answer each question
3. Evaluates answers using multiple metrics (exact/fuzzy/contains + LLM judge)
4. Reports aggregate accuracy and per-category performance
"""

import json
import difflib
import re
import concurrent.futures
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import tiktoken

from evaluation.configs.config import Config
from evaluation.conversation_rag import ConversationRAG
from evaluation.client.langchain_client import LangChainClient


class RAGBenchmark:
    """Comprehensive RAG benchmark system"""

    def __init__(self, config: Config, character: str = "Marina_Volkov",
                 include_attachment: bool = False, k: int = 5, full_context: bool = False, reload: bool = False, use_label: bool = False, hybrid: bool = False):
        """
        Initialize the benchmark system

        Args:
            config: Configuration object
            character: Character name to benchmark
            include_attachment: Whether to include attachment documents in vector store
            k: Number of documents to retrieve
            full_context: Whether to use full context (all documents) instead of RAG
            reload: Whether to force rebuild vector store (skip cache/loading)
            use_label: Whether to use labeled supporting evidence instead of retrieval
            hybrid: Whether to use hybrid retrieval (BM25 + semantic)
        """
        self.config = config
        self.character = character
        self.include_attachment = include_attachment
        self.k = k
        self.full_context = full_context
        self.reload = reload
        self.use_label = use_label
        self.hybrid = hybrid
        self.llm_client = LangChainClient(model=config.model, api_version=config.api_version, enable_langsmith=config.langsmith_enabled)

        # Initialize RAG system
        self.rag_system = ConversationRAG(config)

        # Paths
        self.merged_qa_file = config.data_dir / "qa_pairs" / character / f"{character}_merged.jsonl"

        # Vector store path differs based on whether attachments are included
        store_suffix = "_with_attachments" if include_attachment else ""

        # Add embedding suffix if not using default embedding
        embedding_suffix = ""
        default_embedding = "BAAI/bge-large-en-v1.5"
        if config.embedding and config.embedding != default_embedding:
            safe_embedding = config.embedding.replace('/', '_')
            embedding_suffix = f"_{safe_embedding}"

        self.vector_store_base_path = config.vector_store_dir / f"{character}{store_suffix}{embedding_suffix}"

        self.results_dir = config.results_dir
        self.output_dir = self.results_dir / "output"

        # Create directories
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Cache for date-filtered vector stores
        self._date_vector_store_cache = {}

        # Current context stats
        self.current_context_stats = {
            "conversation_turns": 0,
            "conversation_tokens": 0,
            "attachment_chunks": 0,
            "attachment_tokens": 0,
            "total_tokens": 0
        }

        # Current documents for full context mode
        self.current_docs = []

        # Cache token encoding (creating it per call is expensive)
        try:
            self._tiktoken_encoding = tiktoken.encoding_for_model(self.config.model)
        except Exception:
            self._tiktoken_encoding = tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        return len(self._tiktoken_encoding.encode(text))

    def load_merged_qa_pairs(self) -> Dict[str, Any]:
        """Load QA pairs from the pre-merged JSONL file (if present)."""
        if not self.merged_qa_file.exists():
            raise FileNotFoundError(
                f"Merged QA file not found: {self.merged_qa_file}. "
                "Please provide --input-file (JSONL) or generate the merged file first."
            )
        return self.load_qa_pairs_from_jsonl(self.merged_qa_file)

    def load_qa_pairs_from_jsonl(self, input_file: Union[str, Path]) -> Dict[str, Any]:
        """Load QA pairs from a specified JSONL file (one JSON object per line)."""
        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"JSONL file not found: {input_path}")

        print(f"📥 Loading QA pairs from {input_path}")

        qa_pairs = []
        question_types = Counter()
        qa_format_types = Counter()

        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                qa_data = json.loads(line)
                qa_pairs.append(qa_data)
                question_types[qa_data.get('question_type', 'unknown')] += 1

                if 'options' in qa_data and qa_data.get('options'):
                    qa_format_types['multiple_choice'] += 1
                else:
                    qa_format_types['regular'] += 1

        data = {
            "character": self.character,
            "total_questions": len(qa_pairs),
            "question_types": dict(question_types),
            "qa_format_types": dict(qa_format_types),
            "qa_pairs": qa_pairs,
        }

        print(f"✅ Loaded {data['total_questions']} questions")
        print(f"   Question types: {dict(data['question_types'])}")
        print(f"   QA formats: {dict(data['qa_format_types'])}")

        return data
    
    def prepare_rag_system_for_date(self, cutoff_date: str) -> None:
        """
        Prepare the RAG system with date-filtered documents
        
        Args:
            cutoff_date: Only include documents before this date (YYYY-MM-DD format)
        """
        # Check if we already have this date's vector store in memory (same-run optimization)
        cache_key = f"{cutoff_date}_{self.include_attachment}"
        if not self.reload and not self.full_context and not self.use_label and cache_key in self._date_vector_store_cache:
            self.rag_system.vector_store, self.rag_system.all_documents, self.current_context_stats = self._date_vector_store_cache[cache_key]
            print(f"✅ Using in-memory cached vector store for {cutoff_date}")
            return
        
        print(f"🔧 Preparing RAG system for {self.character} (cutoff: {cutoff_date})...")
        
        # Load conversations with date filter
        documents = self.rag_system.load_conversations(
            character=self.character, 
            cutoff_date=cutoff_date
        )
        
        # Calculate conversation stats
        conv_turns = len(documents)
        conv_tokens = sum(self._count_tokens(d.page_content) for d in documents)
        
        # Optionally load attachments
        att_chunks = 0
        att_tokens = 0
        if self.include_attachment:
            attachment_docs = self.rag_system.load_attachments(
                character=self.character,
                cutoff_date=cutoff_date
            )
            documents.extend(attachment_docs)
            att_chunks = len(attachment_docs)
            att_tokens = sum(self._count_tokens(d.page_content) for d in attachment_docs)
            print(f"   📎 Included {len(attachment_docs)} attachment chunks")
        
        if not documents:
            print(f"⚠️ No documents found before {cutoff_date}")
            self.rag_system.vector_store = None
            self.current_docs = []
            return
        
        # Store documents for full context mode
        self.current_docs = documents
        
        # Calculate stats
        stats = {
            "conversation_turns": conv_turns,
            "conversation_tokens": conv_tokens,
            "attachment_chunks": att_chunks,
            "attachment_tokens": att_tokens,
            "total_tokens": conv_tokens + att_tokens
        }
        self.current_context_stats = stats

        # Build vector store in real-time (no disk caching)
        if not self.full_context and not self.use_label:
            self.rag_system.build_vector_store(documents)

            # Cache the vector store in memory for same-run reuse
            self._date_vector_store_cache[cache_key] = (self.rag_system.vector_store, self.rag_system.all_documents, stats)

            print(f"✅ Vector store ready (in-memory cached for date: {cutoff_date})")
    
    def prepare_rag_system(self) -> None:
        """
        Prepare the RAG system by loading or building vector store (without date filter)
        """
        print(f"🔧 Preparing RAG system for {self.character}...")
        
        # Try to load existing vector store for this character
        # Note: In full_context mode, we cannot skip loading documents because we need them in self.current_docs
        if not self.reload and not self.full_context and not self.use_label and (self.vector_store_base_path / "index.faiss").exists():
            print(f"📥 Loading existing vector store for {self.character}...")
            stats = self.rag_system.load_vector_store(str(self.vector_store_base_path))
            if stats:
                self.current_context_stats = stats
        else:
            print(f"🔨 Building new vector store for {self.character}...")
            # Load conversations for the specific character
            documents = self.rag_system.load_conversations(character=self.character)

            conv_turns = len(documents)
            conv_tokens = sum(self._count_tokens(d.page_content) for d in documents)
            
            # Optionally load attachments
            att_chunks = 0
            att_tokens = 0
            if self.include_attachment:
                attachment_docs = self.rag_system.load_attachments(character=self.character)
                documents.extend(attachment_docs)
                print(f"   📎 Included {len(attachment_docs)} attachment chunks")
                att_chunks = len(attachment_docs)
                att_tokens = sum(self._count_tokens(d.page_content) for d in attachment_docs)
            
            if documents:
                self.current_docs = documents
                stats = {
                    "conversation_turns": conv_turns,
                    "conversation_tokens": conv_tokens,
                    "attachment_chunks": att_chunks,
                    "attachment_tokens": att_tokens,
                    "total_tokens": conv_tokens + att_tokens,
                }
                self.current_context_stats = stats
                if not self.full_context and not self.use_label:
                    self.rag_system.build_vector_store(
                        documents,
                        save_path=str(self.vector_store_base_path),
                        context_stats=stats,
                    )
            else:
                self.current_docs = []
                raise RuntimeError(f"No conversation documents found for {self.character}")
        
        # Display RAG system stats
        stats = self.rag_system.get_stats()
        print(f"📊 RAG System ready for {self.character}:")
        print(f"   Total documents: {stats.get('total_documents', 0)}")
        print(f"   Total conversations: {stats.get('total_conversations', 0)}")
        print(f"   Total attachments: {stats.get('total_attachments', 0)}")
        print(f"   Characters: {', '.join(stats.get('characters', []))}")
        
        # Verify we have the right character data
        if self.character not in stats.get('characters', []):
            print(f"⚠️ Warning: {self.character} not found in loaded characters!")
            print(f"   Available characters: {', '.join(stats.get('characters', []))}")
    
    def exact_match_score(self, predicted: str, expected: str) -> float:
        """
        Calculate exact match score between predicted and expected answers
        
        Args:
            predicted: Predicted answer
            expected: Expected answer
            
        Returns:
            1.0 if exact match, 0.0 otherwise
        """
        # Normalize both strings (lowercase, strip whitespace)
        pred_norm = str(predicted).lower().strip()
        exp_norm = str(expected).lower().strip()
        
        return 1.0 if pred_norm == exp_norm else 0.0
    
    def fuzzy_match_score(self, predicted: str, expected: str) -> float:
        """
        Calculate fuzzy match score using sequence similarity
        
        Args:
            predicted: Predicted answer
            expected: Expected answer
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Normalize strings
        pred_norm = str(predicted).lower().strip()
        exp_norm = str(expected).lower().strip()
        
        # Use difflib to calculate similarity
        similarity = difflib.SequenceMatcher(None, pred_norm, exp_norm).ratio()
        
        return similarity
    
    def contains_answer_score(self, predicted: str, expected: str) -> float:
        """
        Check if predicted answer contains the expected answer
        
        Args:
            predicted: Predicted answer
            expected: Expected answer
            
        Returns:
            1.0 if expected is contained in predicted, 0.0 otherwise
        """
        pred_norm = str(predicted).lower().strip()
        exp_norm = str(expected).lower().strip()
        
        return 1.0 if exp_norm in pred_norm else 0.0
    
    def llm_judge_score(self, question: str, predicted: str, expected: str, question_type: str = "unknown") -> Dict[str, Any]:
        """
        Use LLM as judge to evaluate the answer quality
        
        Args:
            question: Original question
            predicted: Predicted answer
            expected: Expected answer
            question_type: Type of question (e.g. 'safe', 'adversarial' use adversarial prompt)
            
        Returns:
            Dictionary with accuracy_score (0 or 1) and overall_score (0-1)
        """
        prompt = f"""You are an expert evaluator assessing an AI assistant's answer against a reference answer.

Question: {question}
Expected Answer: {expected}
AI Assistant's Answer: {predicted}

Please evaluate the AI assistant's answer on the following criteria:

### Accuracy (0 or 1)
- **1 (Correct)**: The assistant's answer is correct as expected.
- **0 (Incorrect)**: The assistant's answer contradicts the expected answer. 

### Overall Quality (0-10)
- **9-10**: Accurate, complete, well-structured, and directly addresses the question.
- **7-8**: Accurate with minor omissions or slightly verbose.
- **5-6**: Partially correct; contains some relevant information but misses key points.
- **3-4**: Mostly incorrect but shows some understanding of the topic.
- **1-2**: Almost entirely wrong or irrelevant.
- **0**: Completely wrong, refuses to answer, or is incoherent.

Provide your evaluation in the following JSON format:
{{
    "accuracy_score": [0 or 1],
    "overall_score": [0-10]
}}

Only respond with valid JSON, no other text."""
        prompt_adv = f"""You are an expert evaluator assessing an AI assistant's answer against a reference answer.

Question: {question}
Expected Answer: {expected}
AI Assistant's Answer: {predicted}

Please evaluate the AI assistant's answer on the following criteria:

### Accuracy (0 or 1)
- **1**: The assistant explicitly identifies the conflict described in the reference answer AND points out the true situation or the user's actual status (e.g., corrects the false premise, states the real fact, or clarifies what the user actually did/said).
- **0**: The assistant fails to identify the conflict, or identifies it but does not clarify the true situation or user state.

**Overall Quality** (0–10):
- **9-10**: Identifies the conflict, clearly states the true situation or user's actual status, and proposes a well-tailored alternative if question asks.
- **7-8**: Identifies the conflict and partially clarifies the true situation, but with minor omissions or imprecision.
- **5-6**: Mentions the conflict but fails to clearly state the true situation or user's actual status.
- **3-4**: Shows vague awareness of the conflict without identifying it or clarifying the real facts.
- **1-2**: Completely ignores the conflict or provides only irrelevant information.
- **0**: Fails to identify the contradiction and follows the false premise without correction.

Provide your evaluation in the following JSON format:
{{
    "accuracy_score": [0 or 1],
    "overall_score": [0-10]
}}

Only respond with valid JSON, no other text."""
        # Use adversarial prompt for safe/adversarial question types
        active_prompt = prompt_adv if question_type in ("safe", "adversarial") else prompt

        try:
            response = self.llm_client.invoke(active_prompt)
            
            # Try to parse JSON response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            result = json.loads(response)
            
            # Ensure accuracy_score is 0 or 1
            accuracy_raw = result.get("accuracy_score", 0)
            if accuracy_raw not in [0, 1]:
                # If not 0 or 1, convert based on threshold
                accuracy_score = 1.0 if accuracy_raw >= 0.5 else 0.0
            else:
                accuracy_score = float(accuracy_raw)
            
            # Normalize overall_score to 0-1 range
            overall_score = result.get("overall_score", 0) / 10.0
            
            return {
                "accuracy_score": accuracy_score,
                "overall_score": overall_score
            }
            
        except Exception as e:
            print(f"    ❌ LLM judge error: {e}")
            return {
                "accuracy_score": 0.0,
                "overall_score": 0.0
            }
    
    def extract_selected_option(self, response: str, options: Dict[str, str]) -> str:
        """
        Extract the selected option (A, B, C, D) from the model's response
        
        Args:
            response: Model's response text
            options: Dictionary of available options
            
        Returns:
            Selected option letter or "UNKNOWN" if not found
        """
        response_upper = str(response).upper()
        
        # Look for explicit option selections (e.g., "The answer is A", "I select B", etc.)
        for option_key in options.keys():
            patterns = [
                f"ANSWER IS {option_key}",
                f"{option_key}:",
            ]
            
            for pattern in patterns:
                if re.search(pattern, response_upper):
                    return option_key
        
        # If no explicit selection found, look for the first option mentioned
        for option_key in options.keys():
            if option_key in response_upper:
                return option_key
        
        return "UNKNOWN"
    
    def retrieve_labeled_documents(self, supporting_evidence: List[str]) -> List[Any]:
        """
        Retrieve documents based on supporting evidence labels.
        """
        if not supporting_evidence:
            return []
            
        relevant_docs = []
        
        # Parse evidence
        # Formats: "YYYY-MM-DD:turn" or "filename:section" or "filename"
        
        target_turns = set() # (date, turn_str)
        target_files = set() # filename (without extension or with?)
        
        for item in supporting_evidence:
            if ":" in item:
                # Check if it is date:turn
                parts = item.split(":")
                if len(parts) == 2 and re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]):
                     target_turns.add((parts[0], parts[1]))
                else:
                     # Assume filename:section
                     # We match by filename. 
                     # Filename might be "07_report_task_d8d80e26.md"
                     target_files.add(parts[0])
            else:
                # Assume filename
                target_files.add(item)
                
        # Search in current_docs
        for doc in self.current_docs:
            doc_date = doc.metadata.get("date", "unknown")
            doc_turn = str(doc.metadata.get("turn", ""))
            doc_filename = doc.metadata.get("filename", "")
            
            # Check conversation match
            if (doc_date, doc_turn) in target_turns:
                relevant_docs.append(doc)
                continue
                
            # Check attachment match
            # doc_filename might be full path or just name. Metadata usually has name.
            if doc_filename in target_files:
                relevant_docs.append(doc)
                
        return relevant_docs

    def evaluate_single_qa(self, qa_pair: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single QA pair using the RAG system
        
        Args:
            qa_pair: Dictionary containing question and answer (and optionally options for multiple choice)
            
        Returns:
            Evaluation results
        """
        question = qa_pair["question"]
        expected_answer = qa_pair["answer"]
        question_type = qa_pair.get("question_type", "unknown")
        question_date = qa_pair.get("question_date", "unknown")
        
        # Check if this is a multiple choice question
        is_multiple_choice = 'options' in qa_pair and qa_pair.get('options')
        
        if is_multiple_choice:
            print(f"  🔍 Evaluating (MC): {question[:50]}...")
        else:
            print(f"  🔍 Evaluating: {question[:50]}...")
        
        # Get RAG response
        try:
            query_text = question
            oracle_text = None
            if is_multiple_choice:
                # For multiple choice, format the query with options
                options = qa_pair['options']
                formatted_query = f"{question}\n\nOptions:\n"
                for opt_key, opt_value in options.items():
                    formatted_query += f"{opt_key}: {opt_value}\n"
                formatted_query += "\nPlease select the best answer from the options above and explain your reasoning."
                query_text = formatted_query
                oracle_text = question

            if self.full_context:
                rag_response = self.rag_system.generate_response(
                    query=query_text,
                    oracle=oracle_text,
                    character=self.character,
                    full_context_docs=self.current_docs,
                    question_date=question_date,
                    question_type=question_type
                )
            elif self.use_label:
                labeled_docs = self.retrieve_labeled_documents(qa_pair.get("supporting_evidence", []))
                rag_response = self.rag_system.generate_response(
                    query=query_text,
                    oracle=oracle_text,
                    character=self.character,
                    full_context_docs=labeled_docs,
                    question_date=question_date,
                    question_type=question_type
                )
            else:
                rag_response = self.rag_system.generate_response(
                    query=query_text,
                    oracle=oracle_text,
                    character=self.character,
                    k=self.k,
                    question_date=question_date,
                    question_type=question_type,
                    hybrid=self.hybrid
                )
            
            predicted_answer = rag_response["response"]
            
        except Exception as e:
            print(f"    ❌ RAG error: {e}")
            predicted_answer = f"Error: {str(e)}"
            rag_response = {"error": str(e)}
        
        # Calculate evaluation scores
        if is_multiple_choice:
            # For multiple choice, we need to extract the selected option from the response
            selected_option = self.extract_selected_option(predicted_answer, qa_pair['options'])
            
            # For multiple choice questions, compare the selected option with expected answer
            exact_match = 1.0 if selected_option == expected_answer else 0.0
            fuzzy_match = exact_match  # For MC, fuzzy match is same as exact match
            contains_answer = 1.0 if expected_answer in predicted_answer else 0.0
            
            # LLM judge evaluation for multiple choice (concatenate options into question)
            options_text = "\n".join([f"{k}: {v}" for k, v in qa_pair['options'].items()])
            judge_question = f"{question}\n\nOptions:\n{options_text}"
            llm_judge = self.llm_judge_score(judge_question, predicted_answer, expected_answer, question_type=question_type)
        else:
            # Regular evaluation for non-multiple choice questions
            exact_match = self.exact_match_score(predicted_answer, expected_answer)
            fuzzy_match = self.fuzzy_match_score(predicted_answer, expected_answer)
            contains_answer = self.contains_answer_score(predicted_answer, expected_answer)
            
            # LLM judge evaluation
            llm_judge = self.llm_judge_score(question, predicted_answer, expected_answer, question_type=question_type)
        
        result = {
            "id": qa_pair.get("id", ""),
            "question": question,
            "expected_answer": expected_answer,
            "predicted_answer": predicted_answer,
            "no_context_response": rag_response.get("no_context_response", ""),
            "question_type": question_type,
            "is_multiple_choice": is_multiple_choice,
            "cite": qa_pair.get("supporting_evidence", []),
            "difficulty": qa_pair.get("difficulty", "unknown"),
            "question_date": qa_pair.get("question_date", "unknown"),
            "context_stats": self.current_context_stats.copy(),
            "evaluation_scores": {
                "exact_match": exact_match,
                "fuzzy_match": fuzzy_match,
                "contains_answer": contains_answer,
                "llm_judge": llm_judge
            }
        }
        
        if not self.full_context:
            result["rag_response_metadata"] = {
                "retrieved_count": rag_response.get("retrieved_count", 0),
                "character_filter": rag_response.get("character_filter"),
                "sources": rag_response.get("sources", []),
            }
        
        # Add multiple choice specific fields
        if is_multiple_choice:
            result["options"] = qa_pair['options']
            result["selected_option"] = selected_option
            # result["correct_reasoning"] = qa_pair.get("correct_reasoning", "")
            # result["distractor_reasoning"] = qa_pair.get("distractor_reasoning", {})
        
        return result
    
    def run_benchmark(self, limit: Optional[int] = None, output: bool = False,
                     output_type: str = 'json', use_date_filter: bool = True,
                     input_file: Optional[str] = None,
                     output_file: Optional[str] = None,
                      max_workers: int = 10) -> Dict[str, Any]:
        """
        Run the complete benchmark evaluation
        
        Args:
            limit: Optional limit on number of questions to evaluate
            output: Whether to output detailed Q&A results to files
            output_type: Output format type ('json', 'csv', 'csv,json'). Default is 'json'
            use_date_filter: Whether to filter documents by question_date (default True)
            max_workers: Number of parallel workers for evaluation (default: 1)
            
        Returns:
            Complete benchmark results
        """
        print(f"🚀 Starting RAG Benchmark for {self.character}")
        print(f"   Include attachments: {self.include_attachment}")
        print(f"   Use date filter: {use_date_filter}")
        print(f"   Max workers: {max_workers}")
        if input_file:
            print(f"   Input file: {input_file}")
        print("=" * 60)
        
        # Step 1: Load/merge QA pairs
        merged_data = (
            self.load_qa_pairs_from_jsonl(input_file)
            if input_file
            else self.load_merged_qa_pairs()
        )
        qa_pairs = merged_data["qa_pairs"]
        
        if limit:
            qa_pairs = qa_pairs[:limit]
            print(f"📊 Limited evaluation to {limit} questions")
        
        # Step 2: Prepare RAG system (only once if not using date filter)
        if not use_date_filter:
            self.prepare_rag_system()
        
        # Step 3: Run evaluations
        print(f"🔍 Evaluating {len(qa_pairs)} questions...")
        
        results = []
        
        # Group QA pairs by date to handle date filtering correctly in parallel
        qa_groups = defaultdict(list)
        if use_date_filter:
            for qa in qa_pairs:
                date = qa.get("question_date", "unknown")
                qa_groups[date].append(qa)
            # Sort groups by date
            sorted_dates = sorted(qa_groups.keys())
        else:
            # One big group
            qa_groups["all"] = qa_pairs
            sorted_dates = ["all"]

        total_processed = 0
        
        for date_key in sorted_dates:
            group_pairs = qa_groups[date_key]
            
            if use_date_filter and date_key != "unknown":
                print(f"\n   📅 Switching to date filter: {date_key}")
                self.prepare_rag_system_for_date(date_key)
            
            # Process group in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_qa = {executor.submit(self.evaluate_single_qa, qa): qa for qa in group_pairs}
                
                for future in concurrent.futures.as_completed(future_to_qa):
                    qa = future_to_qa[future]
                    try:
                        result = future.result()
                        results.append(result)
                        total_processed += 1
                        print(f"[{total_processed}/{len(qa_pairs)}] Completed: {qa.get('id', 'unknown')}")
                    except Exception as exc:
                        print(f"    ❌ Error processing question {qa.get('id')}: {exc}")
                        # Create an error result to maintain count
                        error_result = {
                            "id": qa.get("id", ""),
                            "question": qa.get("question", ""),
                            "expected_answer": qa.get("answer", ""),
                            "predicted_answer": f"Error: {str(exc)}",
                            "evaluation_scores": {
                                "exact_match": 0.0,
                                "fuzzy_match": 0.0,
                                "contains_answer": 0.0,
                                "llm_judge": {"accuracy_score": 0.0, "overall_score": 0.0}
                            }
                        }
                        results.append(error_result)
                        total_processed += 1
        
        # Step 4: Calculate aggregate metrics
        metrics = self.calculate_metrics(results)
        
        # Step 5: Save results
        attachment_suffix = "_with_attachments" if self.include_attachment else ""
        date_filter_suffix = "_date_filtered" if use_date_filter else ""
        
        benchmark_results = {
            "character": self.character,
            "benchmark_run_at": datetime.now().isoformat(),
            "include_attachment": self.include_attachment,
            "use_date_filter": use_date_filter,
            "max_workers": max_workers,
            "total_questions": len(results),
            "question_types": merged_data["question_types"],
            "qa_format_types": merged_data.get("qa_format_types", {}),
            "aggregate_metrics": metrics,
            "individual_results": results
        }
        
        results_file = (
            Path(output_file)
            if output_file
            else self.results_dir / self.character / f"{self.character}_benchmark_results_{self.config.model}{attachment_suffix}{date_filter_suffix}.json"
        )
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to {results_file}")

        # Optionally emit detailed per-question results (JSON and/or CSV)
        if output:
            self.output_detailed_results(results, merged_data["question_types"], type=output_type)

        return benchmark_results
    
    def calculate_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics from individual results
        
        Args:
            results: List of individual evaluation results
            
        Returns:
            Dictionary of aggregate metrics
        """
        print("📊 Calculating aggregate metrics...")
        
        if not results:
            return {}
        
        # Overall metrics
        exact_matches = [r["evaluation_scores"]["exact_match"] for r in results]
        fuzzy_matches = [r["evaluation_scores"]["fuzzy_match"] for r in results]
        contains_answers = [r["evaluation_scores"]["contains_answer"] for r in results]
        
        # LLM judge metrics
        llm_accuracy = [r["evaluation_scores"]["llm_judge"]["accuracy_score"] for r in results]
        llm_overall = [r["evaluation_scores"]["llm_judge"]["overall_score"] for r in results]
        
        # Metrics by question type
        type_metrics = defaultdict(lambda: {
            "count": 0,
            "exact_match": [],
            "fuzzy_match": [],
            "contains_answer": [],
            "llm_accuracy": [],
            "llm_overall": []
        })
        
        # Metrics by QA format type (multiple choice vs regular)
        format_metrics = defaultdict(lambda: {
            "count": 0,
            "exact_match": [],
            "fuzzy_match": [],
            "contains_answer": [],
            "llm_accuracy": [],
            "llm_overall": []
        })
        
        for result in results:
            qtype = result.get("question_type", "unknown")
            is_mc = result.get("is_multiple_choice", False)
            format_type = "multiple_choice" if is_mc else "regular"
            
            # Question type metrics
            type_metrics[qtype]["count"] += 1
            type_metrics[qtype]["exact_match"].append(result["evaluation_scores"]["exact_match"])
            type_metrics[qtype]["fuzzy_match"].append(result["evaluation_scores"]["fuzzy_match"])
            type_metrics[qtype]["contains_answer"].append(result["evaluation_scores"]["contains_answer"])
            type_metrics[qtype]["llm_accuracy"].append(result["evaluation_scores"]["llm_judge"]["accuracy_score"])
            type_metrics[qtype]["llm_overall"].append(result["evaluation_scores"]["llm_judge"]["overall_score"])
            
            # Format type metrics
            format_metrics[format_type]["count"] += 1
            format_metrics[format_type]["exact_match"].append(result["evaluation_scores"]["exact_match"])
            format_metrics[format_type]["fuzzy_match"].append(result["evaluation_scores"]["fuzzy_match"])
            format_metrics[format_type]["contains_answer"].append(result["evaluation_scores"]["contains_answer"])
            format_metrics[format_type]["llm_accuracy"].append(result["evaluation_scores"]["llm_judge"]["accuracy_score"])
            format_metrics[format_type]["llm_overall"].append(result["evaluation_scores"]["llm_judge"]["overall_score"])
        
        # Calculate averages for each type
        for qtype in type_metrics:
            tm = type_metrics[qtype]
            type_metrics[qtype] = {
                "count": tm["count"],
                "exact_match_avg": sum(tm["exact_match"]) / len(tm["exact_match"]),
                "fuzzy_match_avg": sum(tm["fuzzy_match"]) / len(tm["fuzzy_match"]),
                "contains_answer_avg": sum(tm["contains_answer"]) / len(tm["contains_answer"]),
                "llm_accuracy_avg": sum(tm["llm_accuracy"]) / len(tm["llm_accuracy"]),
                "llm_overall_avg": sum(tm["llm_overall"]) / len(tm["llm_overall"])
            }
        
        # Calculate averages for each format type
        for format_type in format_metrics:
            fm = format_metrics[format_type]
            format_metrics[format_type] = {
                "count": fm["count"],
                "exact_match_avg": sum(fm["exact_match"]) / len(fm["exact_match"]),
                "fuzzy_match_avg": sum(fm["fuzzy_match"]) / len(fm["fuzzy_match"]),
                "contains_answer_avg": sum(fm["contains_answer"]) / len(fm["contains_answer"]),
                "llm_accuracy_avg": sum(fm["llm_accuracy"]) / len(fm["llm_accuracy"]),
                "llm_overall_avg": sum(fm["llm_overall"]) / len(fm["llm_overall"])
            }
        
        # Calculate average context stats
        avg_conv_turns = sum(r.get("context_stats", {}).get("conversation_turns", 0) for r in results) / len(results) if results else 0
        avg_conv_tokens = sum(r.get("context_stats", {}).get("conversation_tokens", 0) for r in results) / len(results) if results else 0
        avg_att_chunks = sum(r.get("context_stats", {}).get("attachment_chunks", 0) for r in results) / len(results) if results else 0
        avg_att_tokens = sum(r.get("context_stats", {}).get("attachment_tokens", 0) for r in results) / len(results) if results else 0
        avg_total_tokens = sum(r.get("context_stats", {}).get("total_tokens", 0) for r in results) / len(results) if results else 0

        metrics = {
            "context_stats": {
                "avg_conversation_turns": avg_conv_turns,
                "avg_conversation_tokens": avg_conv_tokens,
                "avg_attachment_chunks": avg_att_chunks,
                "avg_attachment_tokens": avg_att_tokens,
                "avg_total_tokens": avg_total_tokens
            },
            "overall": {
                "total_questions": len(results),
                "exact_match_accuracy": sum(exact_matches) / len(exact_matches),
                "fuzzy_match_average": sum(fuzzy_matches) / len(fuzzy_matches),
                "contains_answer_accuracy": sum(contains_answers) / len(contains_answers),
                "llm_judge": {
                    "accuracy_average": sum(llm_accuracy) / len(llm_accuracy),
                    "overall_average": sum(llm_overall) / len(llm_overall)
                }
            },
            "by_question_type": dict(type_metrics),
            "by_qa_format": dict(format_metrics)
        }
        
        return metrics
    
    def output_detailed_results(self, results: List[Dict[str, Any]], question_types: Dict[str, int], 
                              type: str = 'json') -> None:
        """
        Output detailed Q&A results to files
        
        Args:
            results: List of individual evaluation results
            question_types: Dictionary of question types and counts
            type: Output format type ('json', 'csv', 'csv,json'). Default is 'json'
        """
        print(f"📝 Outputting detailed results to {self.output_dir}...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_formats = [fmt.strip().lower() for fmt in type.split(',')]
        
        # Output JSON format
        if 'json' in output_formats:
            json_output_file = self.output_dir / f"{self.character}_detailed_qa_{timestamp}.json"
            
            detailed_output = {
                "character": self.character,
                "generated_at": datetime.now().isoformat(),
                "total_questions": len(results),
                "question_types": question_types,
                "detailed_results": results
            }
            
            with open(json_output_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_output, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ JSON detailed results saved to {json_output_file}")
        
        # Output CSV format
        if 'csv' in output_formats:
            csv_output_file = self.output_dir / f"{self.character}_benchmark_summary_{timestamp}.csv"
            
            with open(csv_output_file, 'w', encoding='utf-8') as f:
                # CSV header
                f.write("question_id,question_type,difficulty,question_date,question,expected_answer,predicted_answer,")
                f.write("exact_match,fuzzy_match,contains_answer,llm_accuracy,llm_overall\n")
                
                for i, result in enumerate(results, 1):
                    scores = result['evaluation_scores']
                    llm_scores = scores['llm_judge']
                    
                    # Escape CSV fields
                    def escape_csv(text):
                        if isinstance(text, str):
                            return '"' + text.replace('"', '""') + '"'
                        return str(text)
                    
                    f.write(f"{i},")
                    f.write(f"{escape_csv(result['question_type'])},")
                    f.write(f"{escape_csv(result.get('difficulty', 'unknown'))},")
                    f.write(f"{escape_csv(result.get('question_date', 'unknown'))},")
                    f.write(f"{escape_csv(result['question'])},")
                    f.write(f"{escape_csv(result['expected_answer'])},")
                    f.write(f"{escape_csv(result['predicted_answer'])},")
                    f.write(f"{scores['exact_match']:.3f},")
                    f.write(f"{scores['fuzzy_match']:.3f},")
                    f.write(f"{scores['contains_answer']:.3f},")
                    f.write(f"{llm_scores['accuracy_score']:.3f},")
                    f.write(f"{llm_scores['overall_score']:.3f}\n")
            
            print(f"  ✅ CSV summary saved to {csv_output_file}")
        
        print(f"📁 Detailed outputs saved in {self.output_dir}")
    
    
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        """
        Print a summary of benchmark results
        
        Args:
            results: Complete benchmark results
        """
        print(f"\n📈 Benchmark Results Summary for {results['character']}")
        print("=" * 60)
        
        overall = results["aggregate_metrics"]["overall"]
        
        print(f"📊 Overall Performance ({overall['total_questions']} questions):")
        print(f"   Exact Match Accuracy: {overall['exact_match_accuracy']:.1%}")
        print(f"   Fuzzy Match Average: {overall['fuzzy_match_average']:.1%}")
        print(f"   Contains Answer Accuracy: {overall['contains_answer_accuracy']:.1%}")
        
        print("\n📊 Context Statistics (Average):")
        context_stats = results["aggregate_metrics"].get("context_stats", {})
        print(f"   Conversation Turns: {context_stats.get('avg_conversation_turns', 0):.1f}")
        print(f"   Conversation Tokens: {context_stats.get('avg_conversation_tokens', 0):.1f}")
        if results.get("include_attachment", False):
            print(f"   Attachment Chunks: {context_stats.get('avg_attachment_chunks', 0):.1f}")
            print(f"   Attachment Tokens: {context_stats.get('avg_attachment_tokens', 0):.1f}")
        print(f"   Total Tokens: {context_stats.get('avg_total_tokens', 0):.1f}")
        
        print("\n🤖 LLM Judge Scores:")
        llm = overall["llm_judge"]
        print(f"   Accuracy Average: {llm['accuracy_average']:.1%}")
        print(f"   Overall Average: {llm['overall_average']:.1%}")
        
        print("\n📋 Performance by Question Type:")
        by_type = results["aggregate_metrics"]["by_question_type"]
        for qtype, metrics in by_type.items():
            print(f"   {qtype.upper()} ({metrics['count']} questions):")
            print(f"     • Exact Match: {metrics['exact_match_avg']:.1%}")
            print(f"     • Fuzzy Match: {metrics['fuzzy_match_avg']:.1%}")
            print(f"     • Contains Answer: {metrics['contains_answer_avg']:.1%}")
            print(f"     • LLM Accuracy: {metrics['llm_accuracy_avg']:.1%}")
            print(f"     • LLM Overall: {metrics['llm_overall_avg']:.1%}")
        
        print("\n📝 Performance by QA Format:")
        by_format = results["aggregate_metrics"].get("by_qa_format", {})
        for format_type, metrics in by_format.items():
            format_name = "Multiple Choice" if format_type == "multiple_choice" else "Regular"
            print(f"   {format_name} ({metrics['count']} questions):")
            print(f"     • Exact Match: {metrics['exact_match_avg']:.1%}")
            print(f"     • Fuzzy Match: {metrics['fuzzy_match_avg']:.1%}")
            print(f"     • Contains Answer: {metrics['contains_answer_avg']:.1%}")
            print(f"     • LLM Accuracy: {metrics['llm_accuracy_avg']:.1%}")
            print(f"     • LLM Overall: {metrics['llm_overall_avg']:.1%}")
        
        # Show question type distribution
        print("\n📊 Question Type Distribution:")
        question_types = results["question_types"]
        total_questions = sum(question_types.values())
        for qtype, count in question_types.items():
            percentage = (count / total_questions) * 100
            print(f"   {qtype.upper()}: {count} questions ({percentage:.1f}%)")
        
        # Show QA format distribution
        qa_format_types = results.get("qa_format_types", {})
        if qa_format_types:
            print("\n📝 QA Format Distribution:")
            for format_type, count in qa_format_types.items():
                format_name = "Multiple Choice" if format_type == "multiple_choice" else "Regular"
                percentage = (count / total_questions) * 100
                print(f"   {format_name}: {count} questions ({percentage:.1f}%)")


def main():
    """Main function to run the benchmark with command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description='RAG Benchmark System for Memory Evaluation')
    parser.add_argument('--character', type=str, required=True,
                       help='Character name to benchmark')
    parser.add_argument('--input-file', type=str, required=True,
                       help='Path to input QA JSONL file (one JSON object per line)')
    parser.add_argument('--include-attachment', action='store_true',
                       help='Include attachment documents in vector store')
    parser.add_argument('--no-date-filter', action='store_true',
                       help='Disable date filtering')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of questions to evaluate')
    parser.add_argument('--output', action='store_true',
                       help='Output detailed Q&A results to files')
    parser.add_argument('--output-type', type=str, default='json',
                       help='Output format type: json, csv, or csv,json')
    parser.add_argument('--output-file', type=str, default=None,
                       help='Path to write benchmark results JSON (overrides default)')
    parser.add_argument('--model', type=str, default=None,
                       help='Model to use for evaluation')
    parser.add_argument('--k', type=int, default=5,
                       help='Number of documents to retrieve for RAG (default: 5)')
    parser.add_argument('--full-context', action='store_true',
                       help='Use full context (all documents) instead of RAG')
    parser.add_argument('--use-label', action='store_true',
                       help='Use labeled supporting evidence instead of retrieval')
    parser.add_argument('--hybrid', action='store_true',
                       help='Use hybrid retrieval (BM25 + semantic)')
    parser.add_argument('--reload', action='store_true',
                       help='Reload vector store (force rebuild)')
    parser.add_argument('--max-workers', type=int, default=1,
                       help='Number of parallel workers for evaluation (default: 1)')

    args = parser.parse_args()

    # Support both relative and absolute paths by resolving to absolute path
    input_path = Path(args.input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Create config
    config = Config()
    config.verbose = True
    if args.model:
        config.model = args.model

    use_date_filter = not args.no_date_filter

    print("🚀 RAG Benchmark System")
    print("=" * 60)
    print(f"   Character: {args.character}")
    print(f"   Input file: {input_path}")
    print(f"   Include attachments: {args.include_attachment}")
    print(f"   Use date filter: {use_date_filter}")
    print(f"   RAG k: {args.k}")
    print(f"   Full Context: {args.full_context}")
    print(f"   Use Label: {args.use_label}")
    print(f"   Hybrid Retrieval: {args.hybrid}")
    print(f"   Reload: {args.reload}")
    print(f"   Max workers: {args.max_workers}")
    if args.limit:
        print(f"   Question limit: {args.limit}")
    if args.output_file:
        print(f"   Output file: {args.output_file}")
    print("=" * 60)

    benchmark = RAGBenchmark(
        config,
        character=args.character,
        include_attachment=args.include_attachment,
        k=args.k,
        full_context=args.full_context,
        reload=args.reload,
        use_label=args.use_label,
        hybrid=args.hybrid
    )

    results = benchmark.run_benchmark(
        limit=args.limit,
        output=args.output,
        output_type=args.output_type,
        use_date_filter=use_date_filter,
        input_file=str(input_path),
        output_file=args.output_file,
        max_workers=args.max_workers
    )

    benchmark.print_summary(results)

    print("\n✅ Benchmark completed!")
    print(f"📁 Detailed results saved in {benchmark.results_dir}/")


if __name__ == "__main__":
    main()
