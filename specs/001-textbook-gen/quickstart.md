# Quickstart Guide: AI-Native Textbook with RAG Chatbot

## Prerequisites

- Node.js 18+ for Docusaurus frontend
- Python 3.11+ for backend services
- Access to an LLM API (OpenAI, Azure OpenAI, or compatible)
- Qdrant vector database (can run locally or use cloud version)
- Neon PostgreSQL database (for metadata)

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key
DEBUG=False
```

#### Run Backend Services
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-dotenv openai qdrant-client psycopg2-binary
uvicorn src.api.main:app --reload --port 8000
```

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
Create a `.env` file in the `frontend` directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_QDRANT_URL=your_qdrant_url
```

#### Run Docusaurus Development Server
```bash
cd frontend
npm run start
```

### 4. Initialize Textbook Content

The textbook content should be placed in the `frontend/docs` directory as markdown files:

```
frontend/docs/
├── 01-intro-to-physical-ai.md
├── 02-basics-humanoid-robotics.md
├── 03-ros2-fundamentals.md
├── 04-digital-twin-simulation.md
├── 05-vision-language-action.md
└── 06-capstone-project.md
```

### 5. Initialize Vector Database

Run the embedding script to process textbook content:

```bash
cd backend
python src/utils/embed_textbook.py
```

This will:
- Read all markdown files from the textbook
- Split content into chunks
- Generate embeddings
- Store them in Qdrant

## API Usage Examples

### Query the RAG System
```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?",
    "session_id": "session-123"
  }'
```

### Query with Text Selection
```bash
curl -X POST http://localhost:8000/api/v1/rag/query-by-text \
  -H "Content-Type: application/json" \
  -d '{
    "selected_text": "Physical AI combines robotics with artificial intelligence...",
    "query": "Can you explain this concept further?",
    "session_id": "session-123"
  }'
```

### Get Textbook Chapters
```bash
curl http://localhost:8000/api/v1/textbook/chapters
```

## Development Workflow

### Adding New Chapters
1. Add the markdown file to `frontend/docs/` with proper naming convention
2. Update the sidebar configuration in `frontend/sidebars.js`
3. Re-run the embedding script to update the vector database

### Testing
Backend tests:
```bash
cd backend
python -m pytest tests/
```

Frontend tests:
```bash
cd frontend
npm test
```

### Deployment

#### Frontend to GitHub Pages
```bash
cd frontend
GIT_USER=<your-username> CURRENT_BRANCH=main USE_SSH=true yarn deploy
```

#### Backend to Cloud Platform
The backend can be deployed to any cloud platform that supports Python applications (Heroku, Railway, Vercel, etc.).

## Troubleshooting

### Common Issues

1. **API Rate Limits**: If getting rate limit errors, consider implementing request queuing or using a different API key.

2. **Slow RAG Responses**: Check Qdrant connection and ensure embeddings are properly indexed.

3. **Missing Textbook Content**: Verify that markdown files are in the correct location and properly formatted.

4. **Environment Variables**: Ensure all required environment variables are set in both frontend and backend.

### Performance Optimization

- Implement caching for frequently asked questions
- Use embedding caching to avoid regenerating embeddings
- Optimize chunk size for better retrieval accuracy
- Monitor and optimize database queries