"""
Configuration class for RHELM Benchmark Evaluation
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Configuration class for the RHELM benchmark evaluation tool"""

    # Model configuration
    model: str = "gpt-4o"
    api_version: str = "2024-12-01-preview"

    # Input/Output configuration
    input_file: Optional[Path] = None
    output_file: Optional[Path] = None

    # Data layout (override to point at a different dataset location)
    data_dir: Path = Path("data")
    conversations_dir: Path = Path("data/conversations")
    attachments_dir: Path = Path("data/attachments")
    emails_dir: Path = Path("data/emails")

    # Vector store / results locations
    vector_store_dir: Path = Path(".cache/vector_store")
    results_dir: Path = Path("evaluation/results")

    # Processing configuration
    max_workers: int = 1
    batch_size: int = 10

    # RAG configuration
    embedding: str = "BAAI/bge-large-en-v1.5"
    embedding_cache_folder: Optional[str] = None
    embedding_device: str = "cpu"
    chunk_size: int = 500
    chunk_overlap: int = 50

    # LangSmith configuration (optional tracing)
    langsmith_enabled: bool = False
    langsmith_project: str = "rhelm-benchmark"

    # Debugging
    verbose: bool = False
    debug: bool = False

    def __post_init__(self) -> None:
        # Normalise all path-like fields to Path objects so callers can pass strings.
        self.data_dir = Path(self.data_dir)
        self.conversations_dir = Path(self.conversations_dir)
        self.attachments_dir = Path(self.attachments_dir)
        self.emails_dir = Path(self.emails_dir)
        self.vector_store_dir = Path(self.vector_store_dir)
        self.results_dir = Path(self.results_dir)
