"""LLM service for generating responses using open source models."""

import logging
from typing import List, Dict, Any
from langchain.llms import Ollama
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM models."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.llm = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the LLM."""
        try:
            # Initialize Ollama LLM (assumes Ollama is running locally)
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            
            self.llm = Ollama(
                model=settings.LLM_MODEL,
                callback_manager=callback_manager,
                verbose=True,
                temperature=0.7
            )
            
            logger.info(f"LLM service initialized with model: {settings.LLM_MODEL}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}")
            # Fallback to a simple response generator if Ollama is not available
            self.llm = None
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a response using the LLM with retrieved context."""
        try:
            # Prepare context from retrieved documents
            context = self._prepare_context(context_docs)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            if self.llm is not None:
                # Use Ollama LLM
                response = self.llm(prompt)
            else:
                # Fallback response when LLM is not available
                response = self._fallback_response(query, context_docs)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return self._fallback_response(query, context_docs)
    
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
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create a prompt for the LLM."""
        prompt = f"""You are a helpful AI assistant. Use the following context to answer the user's question. If the context doesn't contain relevant information, say so clearly.

Context:
{context}

Question: {query}

Answer: Provide a comprehensive answer based on the context above. If the context is not sufficient to answer the question, explain what information is missing."""
        
        return prompt
    
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
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the LLM service."""
        try:
            if self.llm is not None:
                # Try a simple generation
                test_response = self.llm("Hello")
                return {
                    "status": "healthy",
                    "model": settings.LLM_MODEL,
                    "test_response_length": len(test_response)
                }
            else:
                return {
                    "status": "degraded",
                    "model": "fallback",
                    "message": "LLM not available, using fallback responses"
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
