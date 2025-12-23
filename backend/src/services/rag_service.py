from typing import List, Dict, Any, Optional
import uuid
import asyncio
import cohere

from src.models.rag_query import SourceChunk
from src.utils.qdrant_client import qdrant_service
from src.utils.config import config
from src.utils.logging import get_logger, RAGException

logger = get_logger(__name__)


class RAGService:
    """
    Service class for handling RAG (Retrieval Augmented Generation)
    using Cohere v5.21 + Qdrant
    """

    def __init__(self):
        if not config.COHERE_API_KEY:
            raise RuntimeError("COHERE_API_KEY is not set")

        self.cohere = cohere.Client(config.COHERE_API_KEY)

    async def query_rag(
        self,
        query_text: str,
        session_id: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a RAG query using textbook embeddings
        """
        try:
            query_embedding = await self._generate_embedding(query_text)
            similar_chunks = await qdrant_service.search_similar(
                query_vector=query_embedding,
                limit=5,
            )

            if not similar_chunks:
                raise RAGException(
                    "No relevant content found in textbook",
                    {"query": query_text},
                )

            context_text = self._prepare_context(similar_chunks, context)
            response_text = await self._generate_response(query_text, context_text)

            avg_similarity = (
                sum(chunk.get("similarity_score", 0.0) for chunk in similar_chunks)
                / max(len(similar_chunks), 1)
            )

            sources = [
                SourceChunk(
                    chapter_slug=chunk.get("chapter_id", ""),
                    text=chunk.get("text_content", ""),
                    similarity_score=chunk.get("similarity_score", 0.0),
                )
                for chunk in similar_chunks
            ]

            return {
                "response": response_text,
                "sources": sources,
                "confidence": avg_similarity,
                "query_id": str(uuid.uuid4()),
            }

        except Exception as e:
            logger.exception("RAG query failed")
            raise RAGException(str(e))

    async def query_by_text_selection(
        self,
        selected_text: str,
        query: str,
        session_id: str,
    ) -> Dict[str, Any]:
        """
        RAG query using user-selected textbook text
        """
        try:
            full_query = f"Based on the following text:\n{selected_text}\n\nQuestion: {query}"
            query_embedding = await self._generate_embedding(full_query)

            similar_chunks = await qdrant_service.search_similar(
                query_vector=query_embedding,
                limit=3,
            )

            if not similar_chunks:
                raise RAGException(
                    "No relevant content found in textbook",
                    {"query": query},
                )

            context_chunks = [selected_text] + [
                chunk.get("text_content", "") for chunk in similar_chunks
            ]

            response_text = await self._generate_response(query, "\n\n".join(context_chunks))

            avg_similarity = (
                sum(chunk.get("similarity_score", 0.0) for chunk in similar_chunks)
                / max(len(similar_chunks), 1)
            )

            sources = [
                SourceChunk(
                    chapter_slug=chunk.get("chapter_id", ""),
                    text=chunk.get("text_content", ""),
                    similarity_score=chunk.get("similarity_score", 0.0),
                )
                for chunk in similar_chunks
            ]

            return {
                "response": response_text,
                "sources": sources,
                "confidence": avg_similarity,
                "query_id": str(uuid.uuid4()),
            }

        except Exception as e:
            logger.exception("Selection-based RAG query failed")
            raise RAGException(str(e))

    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using Cohere
        """
        try:
            result = await asyncio.to_thread(
                self.cohere.embed,
                texts=[text],
                model=config.EMBEDDING_MODEL,
                input_type="search_query",
            )
            return result.embeddings[0]

        except Exception as e:
            logger.exception("Embedding generation failed")
            raise RAGException(str(e))

    def _prepare_context(
        self,
        similar_chunks: List[Dict[str, Any]],
        context: Optional[str] = None,
    ) -> str:
        """
        Convert similar chunks into a single context string
        """
        parts = []

        if context:
            parts.append(f"Additional context:\n{context}")

        for i, chunk in enumerate(similar_chunks, start=1):
            parts.append(f"Source {i}:\n{chunk.get('text_content', '')}")

        return "\n\n".join(parts)

    async def _generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using Cohere v5.21 Chat API
        """
        try:
            prompt = (
                "You are an AI assistant for a textbook on Physical AI and Humanoid Robotics.\n"
                "Answer ONLY using the context below. If the answer is not present, "
                "say: 'I cannot find this information in the textbook.'\n\n"
                f"Context:\n{context}\n\nQuestion:\n{query}"
            )

            response = await asyncio.to_thread(
                self.cohere.chat,
                model="command-a-03-2025",
                message=prompt,
                # parameters={
                #     "max_output_tokens": config.RAG_MAX_TOKENS,
                #     "temperature": config.RAG_TEMPERATURE,
                # }
            )

            return response.text.strip()

        except Exception as e:
            logger.exception("LLM generation failed")
            raise RAGException(str(e))

    async def graceful_degrade_response(self, query_text: str) -> Dict[str, Any]:
        """
        Fallback response if RAG services are unavailable
        """
        return {
            "response": (
                "The AI assistant is temporarily unavailable. "
                "Please consult the textbook directly."
            ),
            "sources": [],
            "confidence": 0.0,
            "query_id": str(uuid.uuid4()),
        }


# Singleton instance
rag_service = RAGService()
