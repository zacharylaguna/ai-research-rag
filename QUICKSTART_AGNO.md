# Quick Start Guide - Agno RAG System

Get your Agno-powered RAG system up and running in 5 minutes!

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
cd ai-research-rag
pip install -r requirements.txt
```

This will install:
- Agno framework
- FastAPI
- ChromaDB
- Sentence Transformers
- Ollama client

### Step 2: Setup Environment

```bash
cp .env.example .env
```

The default settings work out of the box!

### Step 3: Install Ollama (Optional but Recommended)

For better AI responses, install Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Verify it's running
ollama list
```

**Note:** The system works without Ollama but will use fallback responses.

### Step 4: Start the Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Test It!

Open another terminal and try:

```bash
# Health check
curl http://localhost:8000/health

# Add a document
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Agno is a high-performance framework for building AI agents. It is 10,000x faster than LangGraph with 50x less memory usage.",
    "metadata": {"source": "agno_docs"}
  }'

# Query it
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Agno?",
    "top_k": 3
  }'
```

## 🐳 Docker Setup (Alternative)

Prefer Docker? Even easier:

```bash
# Start everything
sudo docker-compose up --build

# That's it! API is at http://localhost:8000
```

## 📊 Interactive API Docs

Visit http://localhost:8000/docs for:
- Interactive API testing
- Full endpoint documentation
- Request/response schemas

## 🧪 Run Tests

Verify everything works:

```bash
python test_agno_migration.py
```

Or use the comprehensive test suite:

```bash
python test_api.py
```

## 🎯 Common Use Cases

### 1. Upload a Text File

```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -F "file=@your_document.txt"
```

### 2. Batch Upload Documents

```python
import requests

documents = [
    {"content": "Document 1 content...", "metadata": {"source": "doc1"}},
    {"content": "Document 2 content...", "metadata": {"source": "doc2"}},
]

response = requests.post(
    "http://localhost:8000/documents/batch",
    json=documents
)
print(response.json())
```

### 3. Query with Context

```python
import requests

query = {
    "query": "What are the main topics discussed?",
    "top_k": 5
}

response = requests.post(
    "http://localhost:8000/query",
    json=query
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['sources'])}")
```

### 4. Get System Statistics

```bash
curl http://localhost:8000/stats
```

### 5. Clear Knowledge Base

```bash
curl -X DELETE http://localhost:8000/documents
```

## 🔧 Configuration

Edit `.env` to customize:

```bash
# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Model Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=llama2

# Ollama Connection
OLLAMA_HOST=http://localhost:11434

# Optional: Use OpenAI instead
# OPENAI_API_KEY=sk-...
```

## 🎨 Switch to Different LLM

### Use OpenAI

1. Set API key in `.env`:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

2. Update `rag_service.py`:
   ```python
   from agno.models.openai import OpenAIChat
   
   self.agent = Agent(
       name="RAG Assistant",
       model=OpenAIChat(id="gpt-4o"),  # or gpt-3.5-turbo
       # ... rest stays the same
   )
   ```

### Use Anthropic Claude

1. Install: `pip install anthropic`

2. Update `rag_service.py`:
   ```python
   from agno.models.anthropic import Claude
   
   self.agent = Agent(
       name="RAG Assistant",
       model=Claude(id="claude-sonnet-4-5"),
       # ... rest stays the same
   )
   ```

## 🐛 Troubleshooting

### Issue: "Module 'agno' not found"

```bash
pip install -r requirements.txt
```

### Issue: "Ollama connection failed"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Issue: "ChromaDB errors"

```bash
# Clear the database
rm -rf ./chroma_db
# Restart the server
```

### Issue: "Slow first query"

The first query downloads the embedding model (~90MB). Subsequent queries are fast.

## 📈 Performance Tips

1. **Use GPU for embeddings** (if available):
   ```python
   # In agno_knowledge.py
   embedder = SentenceTransformerEmbedder(
       model="all-MiniLM-L6-v2",
       device="cuda"  # or "mps" for Mac
   )
   ```

2. **Adjust chunk size** for your documents:
   ```bash
   # In .env or config.py
   CHUNK_SIZE=500  # Smaller for short docs
   CHUNK_OVERLAP=100
   ```

3. **Increase top_k** for better context:
   ```python
   query = {"query": "...", "top_k": 10}
   ```

## 🎓 Next Steps

1. **Read the full README.md** for detailed documentation
2. **Check MIGRATION_GUIDE.md** to understand the Agno migration
3. **Explore Agno docs**: https://docs.agno.com
4. **Try multi-agent features**: Add specialized agents for different tasks
5. **Add monitoring**: Set `AGNO_API_KEY` to track performance at https://app.agno.com

## 💡 Example: Building a Research Assistant

```python
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno_knowledge import CustomChromaKnowledgeBase

# Create knowledge base
kb = CustomChromaKnowledgeBase(path="./research_db")

# Add research papers
kb.add_document(
    content="Your research paper content...",
    metadata={"title": "Paper 1", "year": 2024}
)

# Create agent with web search
agent = Agent(
    name="Research Assistant",
    model=Ollama(id="llama2"),
    tools=[DuckDuckGoTools()],  # Can search web too!
    instructions=[
        "First check the knowledge base",
        "If needed, search the web for recent info",
        "Cite your sources"
    ]
)

# Use it
response = agent.run("What are the latest trends in AI?")
print(response.content)
```

## 🤝 Need Help?

- **Documentation**: Check README.md and MIGRATION_GUIDE.md
- **Agno Docs**: https://docs.agno.com
- **Issues**: Check logs in `./logs/` directory
- **Community**: Agno Discord and GitHub discussions

---

**Happy building with Agno! 🚀**
