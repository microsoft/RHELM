"""
LangChain Client for LLM Integration

This module provides a flexible LangChain-based client for connecting to various
LLM providers (OpenAI, Azure OpenAI, etc.) for the RHELM benchmark evaluation.
"""

import os
from typing import Optional


class LangChainClient:
    """
    LangChain client for LLM access with optional LangSmith integration.
    
    This client supports multiple backends and can be configured for different
    deployment scenarios.
    """
    
    def __init__(self, 
                 model: str = "gpt-4o", 
                 api_version: str = "2024-12-01-preview",
                 enable_langsmith: bool = False,
                 langsmith_project: str = "rhelm-benchmark",
                 langsmith_api_key: Optional[str] = None,
                 langsmith_endpoint: str = "https://api.smith.langchain.com",
                 max_retries: int = 3,
                 verbose: bool = False):
        """
        Initialize the LangChain client.
        
        Args:
            model: Model identifier to use
            api_version: API version for Azure OpenAI
            enable_langsmith: Whether to enable LangSmith tracing
            langsmith_project: LangSmith project name
            langsmith_api_key: LangSmith API key
            langsmith_endpoint: LangSmith endpoint URL
            max_retries: Maximum number of retries for API calls
            verbose: Whether to print setup information
        """
        self.model = model
        self.api_version = api_version
        self.enable_langsmith = enable_langsmith
        self.langsmith_project = langsmith_project
        self.langsmith_api_key = langsmith_api_key
        self.langsmith_endpoint = langsmith_endpoint
        self.max_retries = max_retries
        self.verbose = verbose
        self._llm = None  # Lazy initialization
        
        # Initialize LangSmith if enabled
        if self.enable_langsmith and self.langsmith_api_key:
            self._setup_langsmith()
    
    def _setup_langsmith(self) -> bool:
        """
        Setup LangSmith tracing.
        
        Returns:
            bool: True if LangSmith was successfully configured
        """
        try:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = self.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = self.langsmith_project
            os.environ["LANGCHAIN_ENDPOINT"] = self.langsmith_endpoint
            
            if self.verbose:
                print(f"✓ LangSmith tracing enabled")
                print(f"  Project: {self.langsmith_project}")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"✗ Failed to setup LangSmith: {e}")
            return False
    
    def _initialize_llm(self):
        """Initialize and return LLM instance based on configuration."""
        if self._llm is not None:
            return self._llm
        
        # Try to import and configure based on available credentials
        api_key = os.environ.get("OPENAI_API_KEY")
        azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        
        if azure_endpoint:
            # Use Azure OpenAI
            try:
                from langchain_openai import AzureChatOpenAI
                self._llm = AzureChatOpenAI(
                    deployment_name=self.model,
                    api_version=self.api_version,
                    max_retries=self.max_retries,
                )
            except ImportError:
                raise ImportError("Please install langchain-openai: pip install langchain-openai")
        elif api_key:
            # Use OpenAI directly
            try:
                from langchain_openai import ChatOpenAI
                self._llm = ChatOpenAI(
                    model=self.model,
                    max_retries=self.max_retries,
                )
            except ImportError:
                raise ImportError("Please install langchain-openai: pip install langchain-openai")
        else:
            raise ValueError(
                "No LLM credentials found. Please set either:\n"
                "- OPENAI_API_KEY for OpenAI\n"
                "- AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY for Azure OpenAI"
            )
        
        return self._llm
    
    def invoke(self, prompt: str) -> str:
        """
        Invoke the LLM with a prompt.
        
        Args:
            prompt: The prompt text to send to the LLM
            
        Returns:
            str: The LLM's response text
        """
        llm = self._initialize_llm()
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    
    def disable_langsmith(self) -> None:
        """Disable LangSmith tracing."""
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        
        if self.verbose:
            print("✓ LangSmith tracing disabled")
    
    def get_langsmith_status(self) -> dict:
        """
        Get current LangSmith configuration status.
        
        Returns:
            dict: Current LangSmith configuration
        """
        return {
            "enabled": os.environ.get("LANGCHAIN_TRACING_V2", "false").lower() == "true",
            "api_key_set": bool(os.environ.get("LANGCHAIN_API_KEY")),
            "project": os.environ.get("LANGCHAIN_PROJECT", "default"),
            "endpoint": os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
        }
