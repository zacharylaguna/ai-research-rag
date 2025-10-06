#!/bin/bash
# Start script for Agno RAG System

echo "🚀 Starting Agno RAG System..."

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
echo "✅ Starting FastAPI server..."
python main.py
