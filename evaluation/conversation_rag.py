#!/usr/bin/env python3
"""
RAG-based Conversation Query System using a FAISS Vector Store.

This module implements a Retrieval-Augmented Generation system that:
1. Loads conversation, email and attachment data from the dataset directory
2. Creates embeddings using a configurable embedding model
3. Stores embeddings in a FAISS vector store
4. Retrieves relevant evidence for a query (dense, or hybrid dense + BM25)
5. Generates responses using an LLM conditioned on the retrieved context
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.documents import Document

from evaluation.client.langchain_client import LangChainClient
from evaluation.configs.config import Config


class ConversationRAG:
    """RAG system for querying conversation history."""

    def __init__(
        self,
        config: Config,
        conversations_dir: Optional[str] = None,
        attachments_dir: Optional[str] = None,
        emails_dir: Optional[str] = None,
    ):
        """
        Initialize the RAG system.

        Args:
            config: Configuration object.
            conversations_dir: Directory containing conversation files
                (defaults to ``config.conversations_dir``).
            attachments_dir: Directory containing attachment files
                (defaults to ``config.attachments_dir``).
            emails_dir: Directory containing email files
                (defaults to ``config.emails_dir``).
        """
        self.config = config
        self.conversations_dir = Path(conversations_dir) if conversations_dir else config.conversations_dir
        self.attachments_dir = Path(attachments_dir) if attachments_dir else config.attachments_dir
        self.emails_dir = Path(emails_dir) if emails_dir else config.emails_dir
        self.llm_client = LangChainClient(model=config.model, api_version=config.api_version)

        # Initialize embedding model (built in real time, no on-disk caching here)
        print(f"🔧 Initializing embedding model: {config.embedding}...")
        if config.embedding == "text-embedding-3-large":
            from langchain_openai import OpenAIEmbeddings

            # Credentials are read from the environment (OPENAI_API_KEY / OPENAI_BASE_URL or
            # the Azure equivalents) so no secrets are ever committed to the repository.
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=3072)
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=config.embedding,
                cache_folder=config.embedding_cache_folder,
                model_kwargs={"device": config.embedding_device},
                encode_kwargs={"normalize_embeddings": True},
            )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

        self.vector_store = None
        self.conversation_metadata = {}
        self.attachment_metadata = {}
        self.all_documents = []  # Store all documents for the BM25 retriever
    
    def load_conversations(self, character: Optional[str] = None, 
                          cutoff_date: Optional[str] = None) -> List[Document]:
        """
        Load conversation data and create documents
        
        Args:
            character: Specific character to load (if None, load all)
            cutoff_date: Only include conversations with date before this date (YYYY-MM-DD format)
            
        Returns:
            List of Document objects
        """
        documents = []
        
        if not self.conversations_dir.exists():
            print(f"❌ Conversations directory not found: {self.conversations_dir}")
            return documents
        
        # Determine which characters to process
        if character:
            character_dirs = [self.conversations_dir / character]
        else:
            character_dirs = [d for d in self.conversations_dir.iterdir() if d.is_dir()]
        
        print(f"📂 Loading conversations from {len(character_dirs)} character(s)...")
        if cutoff_date:
            print(f"   📅 Filtering conversations before: {cutoff_date}")
        
        for char_dir in character_dirs:
            if not char_dir.exists():
                print(f"⚠️ Character directory not found: {char_dir}")
                continue
                
            char_name = char_dir.name
            conversation_files = list(char_dir.glob("conversation_*.json"))
            
            print(f"  📋 Processing {len(conversation_files)} conversations for {char_name}")
            
            filtered_count = 0
            for conv_file in conversation_files:
                try:
                    with open(conv_file, 'r', encoding='utf-8') as f:
                        conv_data = json.load(f)
                    
                    # Extract conversation turns and metadata
                    character_name = conv_data.get('character', char_name)
                    date = conv_data.get('date', 'unknown')
                    conversation = conv_data.get('conversation', [])
                    
                    # Apply date filter if specified
                    if cutoff_date and date != 'unknown':
                        if date >= cutoff_date:
                            filtered_count += 1
                            continue  # Skip conversations on or after cutoff date
                    
                    # Process each conversation turn
                    for turn in conversation:
                        turn_id = f"{character_name}_{date}_turn_{turn.get('turn', 0)}"
                        
                        # Create document for user message
                        user_text = f"User ({turn.get('timestamp', '')}): {turn.get('user', '')}"
                        user_doc = Document(
                            page_content=user_text,
                            metadata={
                                'character': character_name,
                                'date': date,
                                'turn': turn.get('turn', 0),
                                'message_type': turn.get('message_type', 'unknown'),
                                'speaker': 'user',
                                'timestamp': turn.get('timestamp', ''),
                                'turn_id': turn_id,
                                'source_file': str(conv_file),
                                'doc_type': 'conversation'
                            }
                        )
                        documents.append(user_doc)
                        
                        # Create document for assistant response
                        assistant_text = f"Assistant ({turn.get('timestamp', '')}): {turn.get('assistant', '')}"
                        assistant_doc = Document(
                            page_content=assistant_text,
                            metadata={
                                'character': character_name,
                                'date': date,
                                'turn': turn.get('turn', 0),
                                'message_type': turn.get('message_type', 'unknown'),
                                'speaker': 'assistant',
                                'timestamp': turn.get('timestamp', ''),
                                'turn_id': turn_id,
                                'source_file': str(conv_file),
                                'doc_type': 'conversation'
                            }
                        )
                        documents.append(assistant_doc)
                    
                    # Store conversation metadata
                    conv_id = f"{character_name}_{date}"
                    self.conversation_metadata[conv_id] = {
                        'character': character_name,
                        'date': date,
                        'total_turns': len(conversation),
                        'message_types': list(set(turn.get('message_type', 'unknown') for turn in conversation)),
                        'profile_file': conv_data.get('profile_file', ''),
                        'event_file': conv_data.get('event_file', ''),
                        'source_file': str(conv_file)
                    }
                    
                except Exception as e:
                    print(f"    ❌ Error processing {conv_file}: {e}")
            
            if cutoff_date and filtered_count > 0:
                print(f"    📅 Filtered out {filtered_count} conversations (date >= {cutoff_date})")
        
        print(f"✅ Loaded {len(documents)} conversation turns")
        return documents
    
    @staticmethod
    def _parse_email_date(filename: str) -> Optional[str]:
        """Extract ``YYYY-MM-DD`` from an email filename like ``01_email_2024_01_01.txt``."""
        match = re.search(r"_(\d{4})_(\d{2})_(\d{2})", filename)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        return None

    @staticmethod
    def _sequence_number(filename: str) -> Optional[int]:
        """Extract the leading sequence number from a filename like ``01_notes_task_x.md``."""
        match = re.match(r"^(\d+)_", filename)
        return int(match.group(1)) if match else None

    @staticmethod
    def _parse_emails(raw_text: str) -> List[str]:
        """Split a raw email file into individual formatted email blocks."""
        blocks = re.split(r"\n=+\n", raw_text)
        emails = []
        for block in blocks:
            block = block.strip()
            if block:
                emails.append(block)
        return emails

    def load_attachments(self, character: Optional[str] = None,
                         cutoff_date: Optional[str] = None) -> List[Document]:
        """
        Load email and attachment documents.

        Emails live in ``emails_dir/<character>/NN_email_YYYY_MM_DD.txt`` and carry their
        date in the filename. The leading sequence number ``NN`` also dates the attachments
        in ``attachments_dir/<character>/NN_<type>_task_<hash>.{md,html}``, which do not encode
        a date themselves.

        Args:
            character: Specific character to load (if None, load all).
            cutoff_date: Only include documents strictly before this date (YYYY-MM-DD).

        Returns:
            List of Document objects.
        """
        documents: List[Document] = []

        # Determine which characters to process from both attachments and emails
        all_characters = set()
        if character:
            all_characters.add(character)
        else:
            for base_dir in (self.attachments_dir, self.emails_dir):
                if base_dir.exists():
                    all_characters.update(d.name for d in base_dir.iterdir() if d.is_dir())

        print(f"📎 Loading attachments and emails from {len(all_characters)} character(s)...")
        if cutoff_date:
            print(f"   📅 Filtering before: {cutoff_date}")

        for char_name in sorted(all_characters):
            emails_char_dir = self.emails_dir / char_name
            attachments_char_dir = self.attachments_dir / char_name

            # 1. Load emails and build the sequence-number -> date lookup used for attachments.
            seq_date_lookup: Dict[int, str] = {}
            email_count = 0

            if emails_char_dir.exists():
                for email_file in sorted(emails_char_dir.glob("*.txt")):
                    date = self._parse_email_date(email_file.name)
                    seq_num = self._sequence_number(email_file.name)
                    if seq_num is not None and date is not None:
                        seq_date_lookup[seq_num] = date

                    if cutoff_date and date and date >= cutoff_date:
                        continue

                    with open(email_file, "r", encoding="utf-8") as f:
                        raw_text = f.read()

                    emails = self._parse_emails(raw_text)
                    if not emails:
                        continue

                    date_label = date or "unknown"
                    full_content = f"Date: {date_label}\n\n" + "\n\n---\n\n".join(emails)
                    chunks = self.text_splitter.split_text(full_content)

                    for i, chunk in enumerate(chunks):
                        documents.append(Document(
                            page_content=chunk,
                            metadata={
                                "character": char_name,
                                "message_type": "email",
                                "speaker": "email",
                                "date": date_label,
                                "source_file": str(email_file),
                                "filename": email_file.name,
                                "chunk_index": i,
                                "total_chunks": len(chunks),
                                "doc_type": "email",
                            },
                        ))
                    email_count += 1

            if email_count > 0:
                print(f"  📧 Loaded {email_count} days of emails for {char_name}")

            # 2. Load attachments, dating each one via the sequence-number lookup.
            if not attachments_char_dir.exists():
                continue

            attachment_files = sorted(
                f for f in attachments_char_dir.iterdir()
                if f.is_file() and f.suffix in (".md", ".html")
            )
            print(f"  📎 Processing {len(attachment_files)} attachments for {char_name}")

            filtered_count = 0
            for att_file in attachment_files:
                seq_num = self._sequence_number(att_file.name)
                attachment_date = seq_date_lookup.get(seq_num) if seq_num is not None else None

                if cutoff_date and attachment_date and attachment_date >= cutoff_date:
                    filtered_count += 1
                    continue

                with open(att_file, "r", encoding="utf-8") as f:
                    content = f.read()

                chunks = self.text_splitter.split_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "character": char_name,
                            "message_type": "attachment",
                            "speaker": "attachment",
                            "date": attachment_date or "unknown",
                            "source_file": str(att_file),
                            "filename": att_file.name,
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                            "doc_type": "attachment",
                        },
                    ))

                att_id = f"{char_name}_{att_file.stem}"
                self.attachment_metadata[att_id] = {
                    "character": char_name,
                    "date": attachment_date or "unknown",
                    "filename": att_file.name,
                    "total_chunks": len(chunks),
                    "source_file": str(att_file),
                }

            if cutoff_date and filtered_count > 0:
                print(f"    📅 Filtered out {filtered_count} attachments (date >= {cutoff_date})")

        print(f"✅ Loaded {len(documents)} attachment/email chunks")
        return documents
    
    def build_vector_store(self, documents: List[Document], save_path: Optional[str] = None,
                           context_stats: Optional[Dict] = None) -> None:
        """
        Build FAISS vector store from documents

        Args:
            documents: List of Document objects
            save_path: Optional path to save the vector store
            context_stats: Optional dictionary with token statistics to save
        """
        if not documents:
            print("❌ No documents to build vector store")
            return

        print(f"🔨 Building vector store with {len(documents)} documents...")

        # Store all documents for BM25 retriever
        self.all_documents = documents

        # Create vector store
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

        print("✅ Vector store built successfully")
        
        # Save vector store if path provided
        if save_path:
            save_path = Path(save_path)
            save_path.mkdir(parents=True, exist_ok=True)
            
            self.vector_store.save_local(str(save_path))
            
            # Save metadata
            metadata_file = save_path / "conversation_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_metadata, f, indent=2, ensure_ascii=False)

            attachment_metadata_file = save_path / "attachment_metadata.json"
            with open(attachment_metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.attachment_metadata, f, indent=2, ensure_ascii=False)
            
            # Save context stats if provided
            if context_stats:
                stats_file = save_path / "context_stats.json"
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(context_stats, f, indent=2, ensure_ascii=False)
                print(f"📊 Context stats saved to {stats_file}")
            
            print(f"💾 Vector store saved to {save_path}")
    
    def load_vector_store(self, load_path: str) -> Optional[Dict]:
        """
        Load existing vector store

        Args:
            load_path: Path to load vector store from

        Returns:
            Context stats dictionary if available, None otherwise
        """
        load_path = Path(load_path)

        if not load_path.exists():
            print(f"❌ Vector store path not found: {load_path}")
            return None

        print(f"📥 Loading vector store from {load_path}...")

        try:
            self.vector_store = FAISS.load_local(
                str(load_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            # Reconstruct all_documents from vector store docstore
            # This is needed for BM25 retriever in hybrid mode
            if hasattr(self.vector_store, 'docstore') and hasattr(self.vector_store.docstore, '_dict'):
                self.all_documents = list(self.vector_store.docstore._dict.values())
                print(f"📚 Loaded {len(self.all_documents)} documents for hybrid retrieval")

            # Load metadata
            metadata_file = load_path / "conversation_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.conversation_metadata = json.load(f)

            attachment_metadata_file = load_path / "attachment_metadata.json"
            if attachment_metadata_file.exists():
                with open(attachment_metadata_file, 'r', encoding='utf-8') as f:
                    self.attachment_metadata = json.load(f)

            # Load context stats if available
            context_stats = None
            stats_file = load_path / "context_stats.json"
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    context_stats = json.load(f)
                print(f"📊 Context stats loaded from {stats_file}")

            print("✅ Vector store loaded successfully")
            return context_stats

        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            return None
    
    def search_conversations(self, query: str, k: int = 5, character: Optional[str] = None) -> List[Tuple[Document, float]]:
        """
        Search for relevant conversations
        
        Args:
            query: Search query
            k: Number of results to return
            character: Filter by specific character
            
        Returns:
            List of (Document, similarity_score) tuples
        """
        if not self.vector_store:
            print("❌ Vector store not initialized")
            return []
        
        print(f"🔍 Searching for: '{query}' (top {k} results)")
        
        # Perform similarity search
        # NOTE: LangChain's FAISS store may not reliably support metadata filtering across versions.
        # To keep behavior stable, we do an over-retrieval and filter client-side when needed.
        if character:
            candidate_k = max(k * 10, 50)
            candidates = self.vector_store.similarity_search_with_score(query, k=candidate_k)
            results = [(doc, score) for doc, score in candidates if doc.metadata.get("character") == character][:k]
        else:
            results = self.vector_store.similarity_search_with_score(query, k=k)
        
        print(f"📋 Found {len(results)} relevant conversations")

        return results

    def search_conversations_hybrid(self, query: str, k: int = 5, character: Optional[str] = None) -> List[Tuple[Document, float]]:
        """
        Search for relevant conversations using hybrid retrieval (BM25 + semantic)

        Args:
            query: Search query
            k: Number of results to return
            character: Filter by specific character

        Returns:
            List of (Document, similarity_score) tuples
        """
        if not self.vector_store:
            print("❌ Vector store not initialized")
            return []

        print(f"🔍 Hybrid searching for: '{query}' (top {k} results)")

        # Filter documents by character if needed
        docs_for_search = self.all_documents if not character else [
            doc for doc in self.all_documents if doc.metadata.get("character") == character
        ]

        if not docs_for_search:
            print(f"⚠️ No documents found for character: {character}")
            return []

        # Create BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(docs_for_search)
        bm25_retriever.k = k

        # Create semantic retriever from vector store
        semantic_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k * 10 if character else k}
        )

        # Create ensemble retriever (50% BM25, 50% semantic)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, semantic_retriever],
            weights=[0.5, 0.5]
        )

        # Get results
        try:
            results_docs = ensemble_retriever.invoke(query)

            # Filter by character if needed (for semantic results)
            if character:
                results_docs = [doc for doc in results_docs if doc.metadata.get("character") == character]

            # Limit to k results
            results_docs = results_docs[:k]

            # Convert to (Document, score) format
            # Since EnsembleRetriever doesn't return scores, we'll use similarity search for scoring
            results_with_scores = []
            for doc in results_docs:
                # Get a score by doing individual similarity search
                try:
                    individual_results = self.vector_store.similarity_search_with_score(doc.page_content, k=1)
                    if individual_results:
                        _, score = individual_results[0]
                        results_with_scores.append((doc, score))
                    else:
                        results_with_scores.append((doc, 0.0))
                except Exception:
                    results_with_scores.append((doc, 0.0))

            print(f"📋 Found {len(results_with_scores)} relevant conversations (hybrid)")
            return results_with_scores

        except Exception as e:
            print(f"❌ Error in hybrid search: {e}")
            # Fallback to regular semantic search
            return self.search_conversations(query, k=k, character=character)

    def generate_response(
        self,
        query: str,
        oracle: Optional[str] = None,
        character: Optional[str] = None,
        k: int = 5,
        full_context_docs: Optional[List[Document]] = None,
        question_date: Optional[str] = None,
        question_type: Optional[str] = None,
        hybrid: bool = False,
    ) -> Dict:
        """
        Generate response using RAG or Full Context

        Args:
            query: User query
            character: Specific character context
            k: Number of similar conversations to retrieve
            full_context_docs: If provided, use these documents as full context instead of RAG
            hybrid: Whether to use hybrid retrieval (BM25 + semantic)

        Returns:
            Dictionary with response and metadata
        """
        context_pieces = []
        sources = []
        retrieved_count = 0
        search_results: List[Tuple[Document, float]] = []

        if full_context_docs:
            # Use full context mode
            print(f"📚 Using Full Context mode with {len(full_context_docs)} documents")
            for i, doc in enumerate(full_context_docs):
                context_pieces.append(f"[Evidence {i+1}] {doc.page_content}")
                sources.append({
                    'character': doc.metadata.get('character', 'unknown'),
                    'date': doc.metadata.get('date', 'unknown'),
                    'turn': doc.metadata.get('turn', 0),
                    'message_type': doc.metadata.get('message_type', 'unknown'),
                    'file_name': doc.metadata.get('filename', 'unknown'),
                    'chunk_index': doc.metadata.get('chunk_index', 0),
                    'speaker': doc.metadata.get('speaker', 'unknown'),
                    'similarity_score': 1.0, # Full context implies perfect relevance
                    'content_preview': doc.page_content
                })
            retrieved_count = len(full_context_docs)
        else:
            # Search for relevant conversations
            search_query = oracle if oracle else query

            if hybrid:
                print("🔎 Using hybrid retrieval for search...")
                search_results = self.search_conversations_hybrid(search_query, k=k, character=character)
            else:
                if oracle:
                    print(f"🔎 Using oracle for search...\n{oracle}")
                search_results = self.search_conversations(search_query, k=k, character=character)

            if not search_results:
                # Generate response without context when no search results found
                try:
                    no_context_prompt = f"""You are an AI assistant. Please provide a helpful response to the user's query without any additional context.

User Query: {query}

Instructions:
1. Provide a direct answer based on your general knowledge
2. Be specific and concise
3. Make your response short and clear, using a phrase or a few words

Response:"""
                    
                    no_context_response = self.llm_client.invoke(no_context_prompt)
                except Exception as e:
                    no_context_response = f"Error generating no-context response: {str(e)}"
                
                return {
                    'query': query,
                    'response': "I couldn't find any relevant conversations to help answer your query.",
                    'no_context_response': no_context_response.strip() if isinstance(no_context_response, str) else "",
                    'sources': [],
                    'character_filter': character
                }
            
            # Prepare context from search results
            for doc, score in search_results:
                context_pieces.append(f"[Score: {score:.3f}] {doc.page_content}")
                sources.append({
                    'character': doc.metadata.get('character', 'unknown'),
                    'date': doc.metadata.get('date', 'unknown'),
                    'turn': doc.metadata.get('turn', 0),
                    'message_type': doc.metadata.get('message_type', 'unknown'),
                    'file_name': doc.metadata.get('filename', 'unknown'),
                    'chunk_index': doc.metadata.get('chunk_index', 0),
                    'speaker': doc.metadata.get('speaker', 'unknown'),
                    'similarity_score': float(score),
                    'content_preview': doc.page_content
                })
            retrieved_count = len(search_results)
        
        # Create prompt for LLM
        context_text = "\n".join(context_pieces)
        
        question_date_text = question_date if question_date else "unknown"
        
        if question_type == "adversarial" or question_type == "safety" :
            prompt = f"""You are an AI assistant that helps analyze user history. Based on the relevant evidence below, please provide the answer to the user's query.
    Question Date: {question_date_text}
    User Query: {query}
    Relevant Evidence:
------------------------Evidence Start------------------------
    {context_text}
------------------------Evidence End------------------------
    1. If the question contains factual errors or contradicts the evidence, explicitly point it out.
    2. If the question cannot be answered based on the evidence, state that clearly.
    3. Otherwise, answer the question directly based on the evidence.

    Answer:"""
        else:
            prompt = f"""You are an AI assistant that helps analyze user history. Based on the relevant evidence below, please provide the answer to the user's query.
    Relevant Evidence:
------------------------Evidence Start------------------------
    {context_text}
------------------------Evidence End------------------------

Question Date: {question_date_text}
User Query: {query}

For multiple choice questions, please select the best option.
For regular questions, please provide a concise and accurate answer.

Answer:"""
    #   Instructions:
    # 1. Use the evidence to inform your response
    # 2. Be specific and reference relevant details from the evidence
    # 3. If you cannot find relevant information, say so clearly
    # 4. Make your response short and clear, using a phrase or a few words    
        # Generate response using LLM
        try:
            response = self.llm_client.invoke(prompt)
            
            # Generate response without context for comparison
            no_context_prompt = f"""You are an AI assistant. Please provide a helpful response to the user's query without any additional context.

Question Date: {question_date_text}

User Query: {query}

Instructions:
1. Provide a direct answer based on your general knowledge
2. Be specific and concise
3. Make your response short and clear, using a phrase or a few words

Response:"""
            
            no_context_response = self.llm_client.invoke(no_context_prompt)
            
            return {
                'query': query,
                'question_date': question_date_text,
                'response': response.strip(),
                'no_context_response': no_context_response.strip(),
                'sources': sources,
                'character_filter': character,
                'context': context_pieces,
                'retrieved_count': retrieved_count,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'query': query,
                'question_date': question_date_text,
                'response': f"Error generating response: {str(e)}",
                'no_context_response': "",
                'sources': sources,
                'context': context_pieces,
                'character_filter': character,
                'error': str(e)
            }
    
    def get_stats(self) -> Dict:
        """Get statistics about the loaded conversations and attachments"""
        if not self.vector_store:
            return {'error': 'Vector store not initialized'}
        
        # Count documents by character
        character_counts = {}
        total_docs = self.vector_store.index.ntotal
        
        # Count conversations by character from metadata
        for conv_id, metadata in self.conversation_metadata.items():
            char = metadata['character']
            character_counts[char] = character_counts.get(char, 0) + 1
        
        # Count attachments
        attachment_counts = {}
        for att_id, metadata in self.attachment_metadata.items():
            char = metadata['character']
            attachment_counts[char] = attachment_counts.get(char, 0) + 1
        
        return {
            'total_documents': total_docs,
            'total_conversations': len(self.conversation_metadata),
            'total_attachments': len(self.attachment_metadata),
            'characters': list(character_counts.keys()),
            'conversations_per_character': character_counts,
            'attachments_per_character': attachment_counts,
            'embedding_model': self.config.embedding,
            'vector_store_type': "FAISS",
            'cache_enabled': True
        }

