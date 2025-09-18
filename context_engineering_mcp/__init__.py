"""Context Engineering MCP - Advanced AI-powered context management for Claude Desktop/Code"""

__version__ = "2.0.0"
__author__ = "Context Engineering Team"

from .api import app
from .models import ContextWindow, ContextSession, PromptTemplate

__all__ = [
    "app",
    "ContextWindow",
    "ContextSession",
    "PromptTemplate",
]