"""Test script to verify Agno migration is working correctly."""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required imports work."""
    logger.info("Testing imports...")
    try:
        import agno
        from agno.agent import Agent
        from agno.models.ollama import Ollama
        from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
        logger.info("✓ Agno imports successful")
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        return False

def test_knowledge_base():
    """Test custom knowledge base initialization."""
    logger.info("Testing knowledge base...")
    try:
        from agno_knowledge import CustomChromaKnowledgeBase
        from config import settings
        
        kb = CustomChromaKnowledgeBase(
            path="./test_chroma_db",
            collection_name="test_collection",
            chunk_size=500,
            chunk_overlap=100
        )
        
        # Test adding a document
        doc_ids = kb.add_document(
            content="This is a test document about artificial intelligence and machine learning.",
            metadata={"source": "test", "type": "unit_test"}
        )
        
        logger.info(f"✓ Added document with {len(doc_ids)} chunks")
        
        # Test searching
        results = kb.search("artificial intelligence", limit=2)
        logger.info(f"✓ Search returned {len(results)} results")
        
        # Clean up
        kb.clear()
        logger.info("✓ Knowledge base test successful")
        return True
        
    except Exception as e:
        logger.error(f"✗ Knowledge base test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rag_service():
    """Test RAG service initialization."""
    logger.info("Testing RAG service...")
    try:
        from rag_service import RAGService
        from models import DocumentUpload, QueryRequest
        
        # Initialize service
        service = RAGService()
        logger.info("✓ RAG service initialized")
        
        # Test adding a document
        doc = DocumentUpload(
            content="Agno is a high-performance framework for building AI agents. It is 10,000x faster than LangGraph.",
            metadata={"source": "test", "topic": "agno"}
        )
        
        result = service.add_document(doc)
        if result["status"] == "success":
            logger.info(f"✓ Document added: {result['chunks_created']} chunks created")
        else:
            logger.error(f"✗ Failed to add document: {result['message']}")
            return False
        
        # Test querying
        query = QueryRequest(query="What is Agno?", top_k=3)
        response = service.query(query)
        
        logger.info(f"✓ Query processed")
        logger.info(f"  Answer length: {len(response.answer)} chars")
        logger.info(f"  Sources: {len(response.sources)}")
        
        # Test stats
        stats = service.get_stats()
        logger.info(f"✓ Stats retrieved: {stats}")
        
        # Clean up
        service.clear_knowledge_base()
        logger.info("✓ RAG service test successful")
        return True
        
    except Exception as e:
        logger.error(f"✗ RAG service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_compatibility():
    """Test that main.py can be imported."""
    logger.info("Testing API compatibility...")
    try:
        # Just test import, don't start server
        import main
        logger.info("✓ main.py imports successfully")
        logger.info("✓ API endpoints should be compatible")
        return True
    except Exception as e:
        logger.error(f"✗ API compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Agno Migration Test Suite")
    logger.info("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Knowledge Base", test_knowledge_base),
        ("RAG Service", test_rag_service),
        ("API Compatibility", test_api_compatibility),
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"\n--- Running: {name} ---")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Test {name} crashed: {e}")
            results.append((name, False))
        logger.info("")
    
    # Summary
    logger.info("=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed! Migration successful!")
        return 0
    else:
        logger.error(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
