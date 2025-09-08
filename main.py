"""FastAPI application for the RAG system."""

import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from contextlib import asynccontextmanager

from config import settings
from models import (
    DocumentUpload, QueryRequest, QueryResponse, 
    DocumentResponse, HealthResponse
)
from rag_service import RAGService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global RAG service instance
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    global rag_service
    
    # Startup
    logger.info("Starting RAG system...")
    try:
        rag_service = RAGService()
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAG system...")

# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="A simple Retrieval-Augmented Generation system using FastAPI, ChromaDB, and LangChain",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with basic information."""
    return HealthResponse(
        status="healthy",
        message="RAG System API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        stats = rag_service.get_stats()
        if stats.get("status") == "error":
            raise HTTPException(status_code=503, detail=stats.get("message"))
        
        return HealthResponse(
            status="healthy",
            message="All services are operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.post("/documents")
async def add_document(document: DocumentUpload):
    """Add a single document to the knowledge base."""
    try:
        result = rag_service.add_document(document)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Failed to add document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/batch")
async def add_documents_batch(documents: List[DocumentUpload]):
    """Add multiple documents to the knowledge base."""
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        result = rag_service.add_documents_batch(documents)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Failed to add documents batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/upload")
async def upload_text_file(file: UploadFile = File(...)):
    """Upload a text file and add it to the knowledge base."""
    try:
        # Check file type
        if not file.content_type.startswith('text/'):
            raise HTTPException(
                status_code=400, 
                detail="Only text files are supported"
            )
        
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Create document with metadata
        document = DocumentUpload(
            content=text_content,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content)
            }
        )
        
        result = rag_service.add_document(document)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(query_request: QueryRequest):
    """Query the knowledge base and get an AI-generated response."""
    try:
        if not query_request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        response = rag_service.query(query_request)
        return response
        
    except Exception as e:
        logger.error(f"Failed to process query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_system_stats():
    """Get system statistics and health information."""
    try:
        stats = rag_service.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents")
async def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    try:
        result = rag_service.clear_knowledge_base()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except Exception as e:
        logger.error(f"Failed to clear knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
