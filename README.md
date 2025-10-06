# Simple RAG System Starter Template (Agno Framework)

A production-ready Retrieval-Augmented Generation (RAG) system built with **Agno**, FastAPI, ChromaDB, and Docker. This template provides a solid foundation for building AI-powered document search and question-answering applications using only open-source technologies.

**Now powered by Agno** - a blazing-fast, lightweight agentic AI framework that's ~10,000x faster than LangGraph with 50x less memory usage.

⭐ **TRUE AGENTIC RAG**: The agent autonomously decides when and how to search the knowledge base!

> **📦 Just Migrated from LangChain?** Check out [`FULL_AGNO_MIGRATION.md`](FULL_AGNO_MIGRATION.md) for what changed!
>
> **🚀 New User?** Start with [`QUICKSTART_AGNO.md`](QUICKSTART_AGNO.md) for a 5-minute setup guide!

## 🚀 Features

- **True Agentic RAG** - Agent autonomously searches knowledge base (not manual retrieval!)
- **Agno Framework** - High-performance SDK for building AI agents (~10,000x faster instantiation)
- **Native Agno Integration** - Uses Agno's built-in knowledge base classes
- **FastAPI** - Modern, fast web framework for building APIs
- **ChromaDB** - Vector database for efficient similarity search
- **Docker** - Containerized deployment
- **Open Source Models** - Uses HuggingFace embeddings and Ollama for LLM
- **Document Upload** - Support for text file uploads and batch processing
- **RESTful API** - Clean API endpoints for all operations
- **Health Monitoring** - Built-in health checks and system statistics
- **Lightweight & Fast** - Minimal memory footprint with blazing-fast performance
- **Model Agnostic** - Works with any LLM provider (Ollama, OpenAI, Anthropic, etc.)
- **Multi-Agent Ready** - Easy to extend with agent teams

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   RAG Service   │────│ Knowledge Base  │
│                 │    │  (Agno Agent)   │    │   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │              ┌─────────────────┐
         │                       └──────────────│   Agno Agent    │
         │                                      │  + Ollama LLM   │
         │                                      └─────────────────┘
┌─────────────────┐
│   Client Apps   │
└─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Ollama (for local LLM) - Optional but recommended
- Agno framework (installed via pip)

### Installing Ollama (Optional)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., Llama 2)
ollama pull llama2
```

## ⚡ Quick Start (5 Minutes)

**New to this project?** Check out [`QUICKSTART_AGNO.md`](QUICKSTART_AGNO.md) for a fast setup guide!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env

# 3. Start the server
python main.py

# 4. Test it!
curl http://localhost:8000/health
```

That's it! Visit http://localhost:8000/docs for interactive API documentation.

## 🛠️ Installation & Setup

### Prerequisites Setup

1. **Install Docker and Docker Compose:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Add your user to docker group (optional, avoids using sudo)
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

2. **Install Ollama (Optional but Recommended):**
```bash
# Install Ollama for better LLM responses
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., Llama 2)
ollama pull llama2

# Verify installation
ollama list
```

### Option 1: Docker Deployment (Recommended)

1. **Setup the project:**
```bash
# Navigate to project directory
cd ai-research-rag

# Create environment file
cp .env.example .env

# Optional: Edit .env with your preferred settings
nano .env
```

2. **Build and start the system:**
```bash
sudo docker-compose up --build
```

### Option 2: Local Development

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Run the application:**
```bash
python main.py
```

## 🚀 Project Management Commands

### Starting the System

**Docker (Background):**
```bash
# Start in background (detached mode)
sudo docker-compose up -d

# Start with build (if you made code changes)
sudo docker-compose up -d --build

# Start and view logs
sudo docker-compose up --build
```

**Local Development:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start the API server
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Stopping the System

**Docker:**
```bash
# Stop all services
sudo docker-compose down

# Stop and remove volumes (clears database)
sudo docker-compose down -v

# Stop and remove everything (images, containers, networks)
sudo docker-compose down --rmi all -v
```

**Local Development:**
```bash
# Press Ctrl+C in the terminal running the server
# Or if running in background, find and kill the process
pkill -f "python main.py"
```

### Rebuilding the System

**Docker (after code changes):**
```bash
# Rebuild and restart
sudo docker-compose down
sudo docker-compose up --build

# Force rebuild (no cache)
sudo docker-compose build --no-cache
sudo docker-compose up

# Rebuild specific service
sudo docker-compose build rag-api
sudo docker-compose up
```

**Local Development:**
```bash
# Update dependencies
pip install -r requirements.txt

# Restart the server (Ctrl+C then python main.py)
# Or if using --reload flag, changes auto-reload
```

### Testing the System

**Automated Testing:**
```bash
# Run the comprehensive test script
python3 test_api.py

# Test with custom base URL
BASE_URL=http://localhost:8000 python3 test_api.py
```

**Manual API Testing:**
```bash
# Health check
curl http://localhost:8000/health

# Add a test document
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test document content", "metadata": {"source": "test"}}'

# Query the system
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this about?", "top_k": 3}'

# Get system statistics
curl http://localhost:8000/stats
```

**Interactive API Documentation:**
- Open browser: `http://localhost:8000/docs`
- Test all endpoints interactively
- View request/response schemas

### Monitoring & Logs

**Docker Logs:**
```bash
# View logs from all services
sudo docker-compose logs

# Follow logs in real-time
sudo docker-compose logs -f

# View logs from specific service
sudo docker-compose logs rag-api

# View last 50 lines
sudo docker-compose logs --tail=50
```

**System Status:**
```bash
# Check running containers
sudo docker-compose ps

# Check system resources
sudo docker stats

# Check API health
curl http://localhost:8000/health
```

### Database Management

**Clear Knowledge Base:**
```bash
# Via API
curl -X DELETE http://localhost:8000/documents

# Or stop system and remove ChromaDB data
sudo docker-compose down
sudo rm -rf ./chroma_db/*
sudo docker-compose up
```

**Backup Database:**
```bash
# Create backup of ChromaDB
tar -czf chroma_backup_$(date +%Y%m%d_%H%M%S).tar.gz ./chroma_db/

# Restore from backup
tar -xzf chroma_backup_YYYYMMDD_HHMMSS.tar.gz
```

### Development Workflow

**Making Code Changes:**
```bash
# 1. Stop the system
sudo docker-compose down

# 2. Make your changes to the code

# 3. Rebuild and start
sudo docker-compose up --build

# 4. Test your changes
python3 test_api.py
```

**Adding New Dependencies:**
```bash
# 1. Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# 2. Rebuild Docker image
sudo docker-compose build --no-cache

# 3. Restart system
sudo docker-compose up
```

### Troubleshooting

**Common Issues:**

1. **Port already in use:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or change port in .env file
echo "API_PORT=8001" >> .env
```

2. **Docker permission denied:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in

# Use sudo with docker commands (required in most environments)
sudo docker-compose up --build
```

3. **ChromaDB issues:**
```bash
# Clear database and restart
sudo docker-compose down -v
sudo rm -rf ./chroma_db
sudo docker-compose up --build
```

4. **LLM not responding:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
sudo systemctl start ollama

# Pull required model
ollama pull llama2
```

5. **Memory issues:**
```bash
# Check system resources
free -h
df -h

# Reduce chunk size in config.py
# CHUNK_SIZE: int = 500  # Reduce from 1000
```

**Debug Mode:**
```bash
# Run with debug logging
LOG_LEVEL=DEBUG sudo docker-compose up

# Or for local development
LOG_LEVEL=DEBUG python3 main.py
```

**Performance Tuning:**
```bash
# Monitor resource usage
sudo docker stats

# Adjust memory limits in docker-compose.yml
# Add under rag-api service:
# mem_limit: 2g
# memswap_limit: 2g
```

## 🔧 Configuration

Edit the `.env` file to customize settings:

```env
# ChromaDB settings
CHROMA_PERSIST_DIRECTORY=./chroma_db

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# Model settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=llama2
```

## 📚 API Usage

The API will be available at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### Key Endpoints

#### Add Document
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your document content here",
    "metadata": {"source": "example.txt"}
  }'
```

#### Upload Text File
```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -F "file=@your_document.txt"
```

#### Query Documents
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 5
  }'
```

#### Get System Stats
```bash
curl -X GET "http://localhost:8000/stats"
```

#### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

## 🧪 Testing

### Quick Test Script

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Add a document
doc_data = {
    "content": "Artificial Intelligence is transforming how we work and live. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions.",
    "metadata": {"topic": "AI", "source": "test"}
}

response = requests.post(f"{base_url}/documents", json=doc_data)
print("Add document:", response.json())

# Query the document
query_data = {
    "query": "What is artificial intelligence?",
    "top_k": 3
}

response = requests.post(f"{base_url}/query", json=query_data)
print("Query response:", response.json())
```

## 🔍 Monitoring

- **Health Check**: `GET /health` - Check system health
- **Statistics**: `GET /stats` - Get detailed system statistics
- **Logs**: Check Docker logs with `docker-compose logs -f`

## 🚀 Deployment

### Production Deployment

1. Set up environment variables for production
2. Configure reverse proxy (nginx, traefik)
3. Set up SSL certificates
4. Configure monitoring and logging
5. Set up backup for ChromaDB data

### Scaling Considerations

- Use external vector database for larger datasets
- Implement caching layer (Redis)
- Add load balancing for multiple API instances
- Consider GPU acceleration for embedding generation

## 🛠️ Customization

### Adding New LLM Providers

Modify `rag_service.py` to add support for other LLM providers with Agno:

```python
# Example: Adding OpenAI support
from agno.models.openai import OpenAIChat

self.agent = Agent(
    name="RAG Assistant",
    model=OpenAIChat(id="gpt-4o"),  # or gpt-3.5-turbo
    # ... rest of configuration
)

# Example: Adding Anthropic Claude
from agno.models.anthropic import Claude

self.agent = Agent(
    name="RAG Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    # ... rest of configuration
)
```

### Custom Document Processing

Extend `agno_knowledge.py` to add custom document preprocessing:

```python
def preprocess_document(self, content: str) -> str:
    # Add your custom preprocessing logic
    # Example: Remove special characters, normalize text, etc.
    content = content.lower()
    content = re.sub(r'[^\w\s]', '', content)
    return processed_content
```

### Why Agno?

**Performance Benefits:**
- **10,000x faster** agent instantiation compared to LangGraph
- **50x less memory** usage for agent operations
- **Native multi-modal** support (text, image, audio, video)
- **Model agnostic** - switch between providers without code changes

**Developer Experience:**
- Simple, pure Python - no graphs or complex chains
- Built-in session management and memory
- Real-time monitoring via agno.com
- Easy multi-agent orchestration

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the logs for error details
- Ensure all dependencies are properly installed
- Verify Ollama is running if using local LLM
