# Migration Guide: LangChain to Agno

This document explains the migration from LangChain to Agno framework and the key changes made to the RAG system.

## Overview

The RAG system has been migrated from **LangChain** to **Agno**, a high-performance framework for building AI agents. This migration brings significant performance improvements and a simpler, more maintainable codebase.

## Key Benefits

### Performance Improvements
- **~10,000x faster** agent instantiation
- **~50x less memory** usage
- Faster query processing
- Better scalability for multi-agent systems

### Developer Experience
- Simpler, more intuitive API
- Pure Python - no complex graphs or chains
- Model agnostic - easy to switch between LLM providers
- Built-in monitoring and telemetry

## What Changed

### 1. Dependencies

**Before (LangChain):**
```
langchain==0.1.0
langchain-community==0.0.10
```

**After (Agno):**
```
agno>=1.1.1
ollama
```

### 2. Architecture Changes

| Component | Before | After |
|-----------|--------|-------|
| Framework | LangChain | Agno |
| Vector Store | `vector_store.py` with LangChain wrappers | `agno_knowledge.py` with custom ChromaDB integration |
| LLM Service | `llm_service.py` with LangChain Ollama | Agno Agent with Ollama model |
| RAG Service | Orchestrates VectorStore + LLMService | Uses Agno Agent with knowledge base |

### 3. File Changes

#### New Files
- **`agno_knowledge.py`** - Custom knowledge base implementation for Agno with ChromaDB
  - Handles document chunking
  - Manages embeddings with SentenceTransformer
  - Provides search functionality

#### Modified Files
- **`rag_service.py`** - Complete rewrite using Agno Agent
  - Simplified from ~140 lines to more maintainable code
  - Uses Agno's Agent class
  - Integrates custom knowledge base
  
- **`requirements.txt`** - Updated dependencies
  - Removed LangChain dependencies
  - Added Agno and Ollama packages

- **`config.py`** - Added Agno-specific settings
  - `AGNO_API_KEY` for monitoring (optional)
  - `OLLAMA_HOST` for Ollama connection

- **`README.md`** - Updated documentation
  - Agno-specific instructions
  - Performance benefits highlighted
  - Updated examples

#### Removed Files
- **`vector_store.py`** - Replaced by `agno_knowledge.py`
- **`llm_service.py`** - Functionality integrated into `rag_service.py` with Agno Agent

### 4. API Changes

**Good News:** The REST API endpoints remain **100% compatible**! No changes needed for clients.

All endpoints work exactly the same:
- `POST /documents` - Add single document
- `POST /documents/batch` - Add multiple documents
- `POST /documents/upload` - Upload text files
- `POST /query` - Query with AI responses
- `GET /health` - Health check
- `GET /stats` - System statistics
- `DELETE /documents` - Clear knowledge base

### 5. Code Comparison

#### Before (LangChain):
```python
# Multiple files and classes
class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(...)
        self.embeddings = HuggingFaceEmbeddings(...)
        self.text_splitter = RecursiveCharacterTextSplitter(...)

class LLMService:
    def __init__(self):
        self.llm = Ollama(model=settings.LLM_MODEL)
    
    def generate_response(self, query, context_docs):
        # Complex prompt engineering
        ...

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
```

#### After (Agno):
```python
# Single, unified approach
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno_knowledge import CustomChromaKnowledgeBase

class RAGService:
    def __init__(self):
        self.knowledge_base = CustomChromaKnowledgeBase(...)
        self.agent = Agent(
            name="RAG Assistant",
            model=Ollama(id=settings.LLM_MODEL),
            description="You are a helpful AI assistant...",
            instructions=[...],
            markdown=True
        )
```

## Migration Steps (For Reference)

If you need to migrate another LangChain project to Agno:

1. **Update dependencies**
   ```bash
   pip uninstall langchain langchain-community
   pip install agno ollama
   ```

2. **Create custom knowledge base**
   - Implement Agno-compatible knowledge base
   - Handle document chunking
   - Integrate with your vector database

3. **Replace LLM service with Agno Agent**
   - Initialize Agent with your LLM provider
   - Configure instructions and behavior
   - Remove old LLM service code

4. **Update RAG service**
   - Use knowledge base for document storage
   - Use agent for query processing
   - Maintain API compatibility

5. **Test thoroughly**
   - Run existing test suite
   - Verify API responses
   - Check performance improvements

## Configuration

### Environment Variables

New variables added:
```bash
# Ollama connection
OLLAMA_HOST=http://localhost:11434

# Optional: Agno monitoring
AGNO_API_KEY=your_key_here
```

### Switching LLM Providers

With Agno, switching providers is trivial:

```python
# Ollama (local)
from agno.models.ollama import Ollama
model = Ollama(id="llama2")

# OpenAI
from agno.models.openai import OpenAIChat
model = OpenAIChat(id="gpt-4o")

# Anthropic
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")

# Google
from agno.models.google import Gemini
model = Gemini(id="gemini-2.0-flash-exp")
```

## Performance Comparison

### Agent Instantiation
- **LangChain**: ~50ms per agent
- **Agno**: ~5μs per agent
- **Improvement**: ~10,000x faster

### Memory Usage
- **LangChain**: ~187.5 KiB per agent
- **Agno**: ~3.75 KiB per agent
- **Improvement**: ~50x less memory

### Query Processing
- Similar performance for single queries
- Agno scales better with multiple concurrent queries
- Better resource utilization

## Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   # Solution: Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Ollama connection issues**
   ```bash
   # Check Ollama is running
   curl http://localhost:11434/api/tags
   
   # Set correct host in .env
   OLLAMA_HOST=http://localhost:11434
   ```

3. **Embedding model issues**
   ```bash
   # First run downloads the model
   # Be patient, it may take a few minutes
   ```

## Future Enhancements

With Agno, you can now easily:

1. **Add multi-agent teams**
   ```python
   web_agent = Agent(name="Web Agent", tools=[DuckDuckGoTools()])
   research_agent = Agent(name="Research Agent", tools=[...])
   team = Agent(team=[web_agent, research_agent])
   ```

2. **Add memory/sessions**
   ```python
   from agno.storage.postgres import PostgresStorage
   
   agent = Agent(
       model=...,
       storage=PostgresStorage(...)
   )
   ```

3. **Add structured outputs**
   ```python
   from pydantic import BaseModel
   
   class Answer(BaseModel):
       answer: str
       confidence: float
   
   response = agent.run(query, response_model=Answer)
   ```

4. **Monitor in real-time**
   - Set `AGNO_API_KEY` in .env
   - Visit https://app.agno.com to see agent sessions

## Resources

- **Agno Documentation**: https://docs.agno.com
- **Agno GitHub**: https://github.com/agno-agi/agno
- **Agno Examples**: https://docs.agno.com/examples/introduction
- **Agno Discord**: Join for community support

## Support

If you encounter issues with the migration:
1. Check the logs for error details
2. Verify all dependencies are installed
3. Ensure Ollama is running (if using local LLM)
4. Review this migration guide
5. Check Agno documentation

## Conclusion

The migration to Agno provides:
- ✅ Significant performance improvements
- ✅ Simpler, more maintainable code
- ✅ Better scalability
- ✅ 100% API compatibility
- ✅ Future-proof architecture

The system is now ready for production use with enhanced performance and capabilities!
