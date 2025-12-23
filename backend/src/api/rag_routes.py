# src/api/rag_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

# Import the ingest service correctly
from src.services.ingest_service import ingest_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/rag",
    tags=["rag"]
)

# Request schema
class RAGQueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[str] = None

# Response schema
class RAGQueryResponse(BaseModel):
    answer: str
    source_chunks: Optional[List[str]] = []

# RAG query endpoint
@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    try:
        logger.info(f"Received RAG query: {request.query}")
        
        # Call the ingest service
        result = await ingest_service.process_query(
            query=request.query,
            session_id=request.session_id,
            context=request.context
        )
        
        # Extract answer and chunks safely
        if isinstance(result, dict):
            answer_text = str(result.get("response", ""))
            chunks = result.get("source_chunks", [])
        elif isinstance(result, (list, tuple)) and len(result) == 2:
            answer_text, chunks = result
            answer_text = str(answer_text)
        else:
            answer_text = str(result)
            chunks = []

        return RAGQueryResponse(answer=answer_text, source_chunks=chunks)
    
    except Exception as e:
        logger.error(f"Error processing RAG query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
