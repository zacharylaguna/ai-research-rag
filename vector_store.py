"""Vector store implementation using ChromaDB."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict, Any
import uuid
import logging
from config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    """ChromaDB vector store for document storage and retrieval."""
    
    def __init__(self):
        """Initialize the vector store."""
        self.client = None
        self.collection = None
        self.embeddings = None
        self.text_splitter = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and collection."""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME
            )
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )
            
            logger.info("Vector store initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None) -> List[str]:
        """Add documents to the vector store."""
        try:
            if metadatas is None:
                metadatas = [{}] * len(documents)
            
            all_chunks = []
            all_metadatas = []
            all_ids = []
            
            for doc_content, metadata in zip(documents, metadatas):
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc_content)
                
                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    chunk_metadata = {
                        **metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "original_doc_length": len(doc_content)
                    }
                    
                    all_chunks.append(chunk)
                    all_metadatas.append(chunk_metadata)
                    all_ids.append(chunk_id)
            
            # Generate embeddings
            embeddings = self.embeddings.embed_documents(all_chunks)
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            
            logger.info(f"Added {len(all_chunks)} chunks from {len(documents)} documents")
            return all_ids
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def similarity_search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            if top_k is None:
                top_k = settings.SIMILARITY_TOP_K
            
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'score': 1 - results['distances'][0][i]  # Convert distance to similarity
                }
                formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} similar documents for query")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": settings.CHROMA_COLLECTION_NAME
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
            self.collection = self.client.create_collection(settings.CHROMA_COLLECTION_NAME)
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise
