"""Test script for the RAG API."""

import requests
import json
import time

def test_rag_api():
    """Test the RAG API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing RAG API...")
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test adding a document
    print("\n2. Testing document addition...")
    doc_data = {
        "content": """
        Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
        that can perform tasks that typically require human intelligence. These tasks include learning, 
        reasoning, problem-solving, perception, and language understanding.
        
        Machine Learning is a subset of AI that focuses on the development of algorithms and statistical 
        models that enable computers to improve their performance on a specific task through experience, 
        without being explicitly programmed for every scenario.
        
        Deep Learning is a subset of machine learning that uses neural networks with multiple layers 
        to model and understand complex patterns in data. It has been particularly successful in areas 
        like image recognition, natural language processing, and speech recognition.
        """,
        "metadata": {
            "topic": "AI/ML",
            "source": "test_document",
            "author": "Test System"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/documents", json=doc_data)
        print(f"Add document: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Add document failed: {e}")
        return
    
    # Add another document
    print("\n3. Adding second document...")
    doc_data2 = {
        "content": """
        Python is a high-level, interpreted programming language known for its simplicity and readability. 
        It was created by Guido van Rossum and first released in 1991. Python supports multiple programming 
        paradigms, including procedural, object-oriented, and functional programming.
        
        Python is widely used in various domains including web development, data science, artificial 
        intelligence, scientific computing, and automation. Its extensive standard library and rich 
        ecosystem of third-party packages make it a popular choice for developers.
        
        Some popular Python frameworks include Django and Flask for web development, NumPy and Pandas 
        for data analysis, and TensorFlow and PyTorch for machine learning.
        """,
        "metadata": {
            "topic": "Programming",
            "source": "test_document_2",
            "author": "Test System"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/documents", json=doc_data2)
        print(f"Add second document: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Add second document failed: {e}")
    
    # Wait a moment for indexing
    time.sleep(2)
    
    # Test querying
    print("\n4. Testing queries...")
    
    queries = [
        "What is artificial intelligence?",
        "Tell me about machine learning",
        "What programming language is good for AI?",
        "How does deep learning work?"
    ]
    
    for query in queries:
        print(f"\n   Query: {query}")
        query_data = {
            "query": query,
            "top_k": 3
        }
        
        try:
            response = requests.post(f"{base_url}/query", json=query_data)
            if response.status_code == 200:
                result = response.json()
                print(f"   Answer: {result['answer'][:200]}...")
                print(f"   Sources found: {len(result['sources'])}")
            else:
                print(f"   Query failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   Query failed: {e}")
    
    # Test stats
    print("\n5. Testing system stats...")
    try:
        response = requests.get(f"{base_url}/stats")
        print(f"Stats: {response.status_code} - {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Stats failed: {e}")
    
    print("\n✅ API testing completed!")

if __name__ == "__main__":
    test_rag_api()
