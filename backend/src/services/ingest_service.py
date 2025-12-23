from typing import List
import logging

from ..utils.textbook_loader import textbook_loader
from .embedding_service import embedding_service
from src.utils.qdrant_client import qdrant_service
from .rag_service import rag_service  # Import the RAG service for queries

logger = logging.getLogger(__name__)


class IngestService:
    def ingest_textbook(self):
        """
        Load textbook markdown → chunk → embed → store in Qdrant
        """
        chapters = textbook_loader.load_chapters_from_directory()

        if not chapters:
            logger.warning("No chapters found for ingestion")
            return {"status": "no_content"}

        total_chunks = 0

        for chapter in chapters:
            text = chapter["content"]
            title = chapter["title"]
            slug = chapter["slug"]

            chunks = self._chunk_text(text)

            embeddings = embedding_service.embed_texts(chunks)

            qdrant_service.upsert_texts(
                texts=chunks,
                embeddings=embeddings,
                metadata={
                    "chapter": title,
                    "slug": slug,
                },
            )

            total_chunks += len(chunks)

        logger.info(f"Ingested {total_chunks} chunks into Qdrant")
        return {"status": "success", "chunks": total_chunks}

    def _chunk_text(self, text: str, size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += size - overlap

        return chunks

    async def process_query(self, query: str, session_id: str, context: str = None):
        """
        Wrapper to call RAG service for a query
        Maps 'query' keyword to RAG service 'query_text'
        """
        try:
            result = await rag_service.query_rag(
                query_text=query,
                session_id=session_id,
                context=context
            )
            return result
        except Exception as e:
            logger.exception("RAG query failed in IngestService")
            return {
                "response": "Error processing query",
                "sources": [],
                "confidence": 0.0
            }


# Singleton instance
ingest_service = IngestService()
