"""Pydantic models for API requests and responses."""

from pydantic import BaseModel
from typing import List, Optional

class DocumentUpload(BaseModel):
    """Model for document upload request."""
    content: str
    metadata: Optional[dict] = {}

class QueryRequest(BaseModel):
    """Model for query request."""
    query: str
    top_k: Optional[int] = 5

class DocumentResponse(BaseModel):
    """Model for document response."""
    id: str
    content: str
    metadata: dict
    score: Optional[float] = None

class QueryResponse(BaseModel):
    """Model for query response."""
    answer: str
    sources: List[DocumentResponse]
    query: str

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    message: str
