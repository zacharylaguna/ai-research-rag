"""Main RAG service that orchestrates document retrieval and response generation."""

import logging
from typing import List, Dict, Any
from vector_store import VectorStore
from llm_service import LLMService
from models import DocumentUpload, QueryRequest, QueryResponse, DocumentResponse

logger = logging.getLogger(__name__)

class RAGService:
    """Main RAG service for document ingestion and querying."""
    
    def __init__(self):
        """Initialize the RAG service."""
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
        logger.info("RAG service initialized")
    
    def add_document(self, document: DocumentUpload) -> Dict[str, Any]:
        """Add a document to the knowledge base."""
        try:
            # Add document to vector store
            doc_ids = self.vector_store.add_documents(
                documents=[document.content],
                metadatas=[document.metadata]
            )
            
            return {
                "status": "success",
                "message": f"Document added successfully",
                "document_ids": doc_ids,
                "chunks_created": len(doc_ids)
            }
            
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            return {
                "status": "error",
                "message": f"Failed to add document: {str(e)}"
            }
    
    def add_documents_batch(self, documents: List[DocumentUpload]) -> Dict[str, Any]:
        """Add multiple documents to the knowledge base."""
        try:
            contents = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            doc_ids = self.vector_store.add_documents(
                documents=contents,
                metadatas=metadatas
            )
            
            return {
                "status": "success",
                "message": f"Added {len(documents)} documents successfully",
                "document_ids": doc_ids,
                "total_chunks_created": len(doc_ids)
            }
            
        except Exception as e:
            logger.error(f"Failed to add documents batch: {e}")
            return {
                "status": "error",
                "message": f"Failed to add documents: {str(e)}"
            }
    
    def query(self, query_request: QueryRequest) -> QueryResponse:
        """Process a query and return a response with sources."""
        try:
            # Retrieve relevant documents
            retrieved_docs = self.vector_store.similarity_search(
                query=query_request.query,
                top_k=query_request.top_k
            )
            
            # Generate response using LLM
            answer = self.llm_service.generate_response(
                query=query_request.query,
                context_docs=retrieved_docs
            )
            
            # Format sources
            sources = [
                DocumentResponse(
                    id=doc['id'],
                    content=doc['content'],
                    metadata=doc['metadata'],
                    score=doc['score']
                )
                for doc in retrieved_docs
            ]
            
            return QueryResponse(
                answer=answer,
                sources=sources,
                query=query_request.query
            )
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            return QueryResponse(
                answer=f"Sorry, I encountered an error while processing your query: {str(e)}",
                sources=[],
                query=query_request.query
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        try:
            vector_stats = self.vector_store.get_collection_stats()
            llm_health = self.llm_service.health_check()
            
            return {
                "vector_store": vector_stats,
                "llm_service": llm_health,
                "status": "operational"
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def clear_knowledge_base(self) -> Dict[str, Any]:
        """Clear all documents from the knowledge base."""
        try:
            self.vector_store.clear_collection()
            return {
                "status": "success",
                "message": "Knowledge base cleared successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            return {
                "status": "error",
                "message": f"Failed to clear knowledge base: {str(e)}"
            }
