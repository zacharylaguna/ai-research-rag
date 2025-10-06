#!/bin/bash
# Start script for Agno RAG System

echo "🚀 Starting Agno RAG System..."

# Check if port 8000 is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use!"
    echo "To stop the existing server, run:"
    echo "  sudo pkill -f 'python main.py'"
    exit 1
fi

# Activate virtual environment
if [ -d "env" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
else
    echo "❌ Virtual environment not found. Please run: python3 -m venv env && source env/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if dependencies are installed
if ! python -c "import agno" 2>/dev/null; then
    echo "❌ Dependencies not installed. Installing..."
    pip install -r requirements.txt
fi

# Start the application
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo ""
echo "To stop the server:"
echo "  • Press Ctrl+C"
echo "  • Or run: sudo pkill -f 'python main.py'"
echo ""
python main.py
