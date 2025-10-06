"""Main RAG service using Agno framework with true agentic RAG."""

import logging
from typing import List, Dict, Any
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno_knowledge import AgnoRAGKnowledgeBase
from models import DocumentUpload, QueryRequest, QueryResponse, DocumentResponse
from config import settings

logger = logging.getLogger(__name__)

class RAGService:
    """Main RAG service with true Agno agentic RAG - agent autonomously searches knowledge."""
    
    def __init__(self):
        """Initialize the RAG service with Agno agent and native knowledge base."""
        # Initialize Agno native knowledge base
        self.knowledge_base = AgnoRAGKnowledgeBase(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            collection_name=settings.CHROMA_COLLECTION_NAME,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Initialize Agno agent
        try:
            self.agent = Agent(
                name="RAG Assistant",
                model=Ollama(id=settings.LLM_MODEL),
                description="You are a helpful AI assistant that answers questions based on provided context.",
                instructions=[
                    "Always base your answers on the context provided.",
                    "If the context doesn't contain relevant information, clearly state that.",
                    "Be concise, accurate, and cite specific information when possible."
                ],
                markdown=True
            )
            self.llm_available = True
            logger.info("RAG service initialized with Agno agent and Ollama")
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama LLM: {e}. Using fallback mode.")
            self.agent = None
            self.llm_available = False
        
        logger.info("RAG service initialized")
    
    def add_document(self, document: DocumentUpload) -> Dict[str, Any]:
        """Add a document to the knowledge base."""
        try:
            # Add document to knowledge base (Agno handles chunking)
            doc_ids = self.knowledge_base.add_text_document(
                content=document.content,
                metadata=document.metadata
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
            
            doc_ids = self.knowledge_base.add_text_documents(
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
        """Process a query with RAG - retrieve context and generate response."""
        try:
            # Retrieve relevant documents from knowledge base
            retrieved_docs = self.knowledge_base.search(
                query=query_request.query,
                limit=query_request.top_k
            )
            
            if self.llm_available and self.agent:
                # Prepare context from retrieved documents
                context = self._prepare_context(retrieved_docs)
                
                # Create prompt with context
                prompt = f"""Context from knowledge base:
{context}

Question: {query_request.query}

Please answer the question based on the context provided above."""
                
                # Get response from Agno agent
                logger.info(f"Processing query with Agno agent: {query_request.query}")
                response = self.agent.run(prompt)
                
                # Extract answer from response
                if hasattr(response, 'content'):
                    answer = response.content
                else:
                    answer = str(response)
            else:
                # Fallback response when agent is not available
                answer = self._fallback_response(query_request.query, retrieved_docs)
            
            # Format sources
            sources = [
                DocumentResponse(
                    id=doc.get('id', 'unknown'),
                    content=doc.get('content', ''),
                    metadata=doc.get('metadata', {}),
                    score=doc.get('score', 0.0)
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
            import traceback
            traceback.print_exc()
            return QueryResponse(
                answer=f"Sorry, I encountered an error while processing your query: {str(e)}",
                sources=[],
                query=query_request.query
            )
    
    def _prepare_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """Prepare context string from retrieved documents."""
        if not context_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            content = doc.get('content', '')
            score = doc.get('score', 0)
            context_parts.append(f"Document {i} (relevance: {score:.2f}):\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _fallback_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a fallback response when LLM is not available."""
        if not context_docs:
            return f"I found no relevant documents to answer your question: '{query}'. Please try rephrasing your question or add more documents to the knowledge base."
        
        # Simple extractive response
        best_doc = context_docs[0] if context_docs else None
        if best_doc:
            content = best_doc.get('content', '')
            score = best_doc.get('score', 0)
            
            return f"""Based on the most relevant document (similarity: {score:.2f}), here's what I found:

{content[:500]}{'...' if len(content) > 500 else ''}

Note: This is a simplified response. For better answers, please ensure Ollama is running with the '{settings.LLM_MODEL}' model."""
        
        return "I couldn't generate a proper response. Please check if the LLM service is properly configured."
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        try:
            kb_stats = self.knowledge_base.get_stats()
            
            llm_status = {
                "status": "healthy" if self.llm_available else "degraded",
                "model": settings.LLM_MODEL if self.llm_available else "fallback",
                "framework": "Agno"
            }
            
            return {
                "knowledge_base": kb_stats,
                "llm_service": llm_status,
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
            self.knowledge_base.clear_knowledge_base()
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
