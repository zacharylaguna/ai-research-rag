"""Agno-compatible knowledge base implementation with ChromaDB."""

import logging
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class AgnoRAGKnowledgeBase:
    """Agno-compatible knowledge base with ChromaDB for agentic RAG."""
    
    def __init__(
        self,
        path: str = "./chroma_db",
        collection_name: str = "documents",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """Initialize the knowledge base."""
        self.path = path
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        
        # Initialize embedder
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        logger.info(f"AgnoRAGKnowledgeBase initialized with collection: {collection_name}")
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def add_text_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        """Add a text document to the knowledge base."""
        if metadata is None:
            metadata = {}
        
        try:
            # Chunk the document
            chunks = self._chunk_text(content)
            chunk_ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                chunk_metadata = {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "original_doc_length": len(content)
                }
                
                # Generate embedding
                embedding = self.embedder.encode(chunk).tolist()
                
                # Add to ChromaDB
                self.collection.add(
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[chunk_metadata],
                    ids=[chunk_id]
                )
                
                chunk_ids.append(chunk_id)
            
            logger.info(f"Added document with {len(chunks)} chunks")
            return chunk_ids
            
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            raise
    
    def add_text_documents(self, documents: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add multiple text documents to the knowledge base."""
        if metadatas is None:
            metadatas = [{}] * len(documents)
        
        all_ids = []
        for doc, metadata in zip(documents, metadatas):
            ids = self.add_text_document(doc, metadata)
            all_ids.extend(ids)
        
        return all_ids
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name,
                "path": self.path,
                "type": "AgnoRAGKnowledgeBase"
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)
            logger.info("Knowledge base cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            raise
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Manual search method for fallback scenarios."""
        try:
            # Generate query embedding
            query_embedding = self.embedder.encode(query).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    result = {
                        'id': results['ids'][0][i],
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0,
                        'score': 1 - results['distances'][0][i] if results['distances'] else 1.0
                    }
                    formatted_results.append(result)
            
            return formatted_results
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return []
