# Research Summary: AI-Native Textbook with RAG Chatbot

## Decision: Technology Stack Selection
**Rationale**: Selected a web-based architecture with Docusaurus frontend and FastAPI backend to meet the requirements of serving textbook content with RAG functionality while maintaining separation of concerns.

**Alternatives considered**:
- Single monolithic application: Would mix static content delivery with RAG processing, making deployment and scaling more complex
- Pure static site with client-side RAG: Not feasible due to computational requirements and security concerns
- Native mobile app: Would limit accessibility and increase development complexity

## Decision: RAG Implementation Approach
**Rationale**: Using Qdrant for vector storage and OpenAI-compatible API for embeddings generation to provide accurate textbook-based answers while operating within free-tier constraints.

**Alternatives considered**:
- In-memory storage: Not persistent and doesn't scale
- Local vector databases (like ChromaDB): Less robust for production use
- Custom embedding solution: More complex than needed, better to leverage established tools

## Decision: Deployment Strategy
**Rationale**: Frontend on GitHub Pages for cost-effective static hosting and backend services on a cloud platform (that supports free tier) to handle RAG processing separately.

**Alternatives considered**:
- Full static site with RAG in browser: Computationally infeasible and would expose API keys
- Server-side rendering all content: More expensive and complex than necessary
- Single deployment platform: Would not allow optimal resource allocation for different components

## Decision: Content Management
**Rationale**: Using Docusaurus with markdown files for textbook content to provide easy content management and auto-generated navigation sidebar.

**Alternatives considered**:
- Database-stored content: More complex for static textbook content
- Headless CMS: Adds unnecessary complexity for this use case
- Custom content management: Reinventing existing solutions

## Decision: API Architecture
**Rationale**: RESTful API with FastAPI for backend services to handle RAG requests, textbook content, and user interactions with proper documentation via OpenAPI.

**Alternatives considered**:
- GraphQL: More complexity than needed for this use case
- Serverless functions: Could work but FastAPI provides better structure for this application
- Direct database access from frontend: Security and performance concerns

## Key Findings

### Performance Considerations
- Qdrant is efficient for similarity search and works well within free-tier constraints
- Response times can be optimized with proper embedding strategies and caching
- Frontend and backend separation allows independent scaling

### Free-Tier Compliance
- Qdrant offers a free tier that should handle textbook-sized content
- Neon PostgreSQL provides free tier options for metadata storage
- OpenAI API or compatible services (like Azure OpenAI, OpenRouter) have usage tiers that work for educational applications

### Security
- Backend API should validate all requests and implement rate limiting
- Frontend should not expose API keys directly
- Proper authentication can be added later if needed

## Risks and Mitigations

### Performance Risk
- **Risk**: RAG responses might exceed 2-3 second target
- **Mitigation**: Proper indexing, caching, and embedding optimization

### Scalability Risk
- **Risk**: 100 concurrent users might exceed free-tier limits
- **Mitigation**: Implement queuing, caching, and resource optimization

### Accuracy Risk
- **Risk**: RAG system might not achieve 90%+ accuracy
- **Mitigation**: Proper embedding techniques, prompt engineering, and quality control of textbook content