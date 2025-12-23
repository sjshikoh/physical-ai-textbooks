from typing import List, Dict, Any
import asyncio
import logging
import cohere

from ..utils.qdrant_client import qdrant_service
from ..utils.config import config
from ..utils.logging import get_logger, RAGException

logger = get_logger(__name__)


class EmbeddingService:
    """
    Service class for handling embedding operations using Cohere
    """

    def __init__(self):
        if not config.COHERE_API_KEY:
            raise RuntimeError(
                "COHERE_API_KEY is not set. Please export COHERE_API_KEY."
            )

        self.cohere = cohere.Client(config.COHERE_API_KEY)

    async def generate_embeddings_for_chapter(
        self,
        chapter_id: str,
        content: str,
        chunk_size: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a textbook chapter
        """
        try:
            chunks = self._split_content_into_chunks(content, chunk_size)

            embeddings_data = []
            for chunk in chunks:
                vector = await self._generate_single_embedding(chunk)
                embeddings_data.append(
                    {
                        "text_content": chunk,
                        "vector": vector,
                    }
                )

            logger.info(
                f"Generated {len(embeddings_data)} embeddings for chapter {chapter_id}"
            )
            return embeddings_data

        except Exception as e:
            logger.error(
                f"Error generating embeddings for chapter {chapter_id}: {e}"
            )
            raise RAGException(f"Error generating embeddings: {str(e)}")

    async def store_chapter_embeddings(
        self,
        chapter_id: str,
        content: str,
        chunk_size: int = 1000
    ):
        """
        Generate and store embeddings for a textbook chapter
        """
        try:
            embeddings_data = await self.generate_embeddings_for_chapter(
                chapter_id, content, chunk_size
            )

            await qdrant_service.store_embeddings(
                chapter_id, embeddings_data
            )

            logger.info(
                f"Stored embeddings for chapter {chapter_id} successfully"
            )

        except Exception as e:
            logger.error(
                f"Error storing embeddings for chapter {chapter_id}: {e}"
            )
            raise RAGException(f"Error storing embeddings: {str(e)}")

    async def update_chapter_embeddings(
        self,
        chapter_id: str,
        content: str,
        chunk_size: int = 1000
    ):
        """
        Update embeddings for a textbook chapter
        """
        try:
            await qdrant_service.delete_embeddings_by_chapter(chapter_id)
            await self.store_chapter_embeddings(
                chapter_id, content, chunk_size
            )

            logger.info(
                f"Updated embeddings for chapter {chapter_id} successfully"
            )

        except Exception as e:
            logger.error(
                f"Error updating embeddings for chapter {chapter_id}: {e}"
            )
            raise RAGException(f"Error updating embeddings: {str(e)}")

    def _split_content_into_chunks(
        self,
        content: str,
        chunk_size: int
    ) -> List[str]:
        """
        Split content into sentence-aware chunks
        """
        sentences = content.split(". ")
        chunks: List[str] = []
        current_chunk = ""

        for sentence in sentences:
            sentence_with_period = (
                sentence + ". "
                if sentence != sentences[-1]
                else sentence
            )

            if len(current_chunk) + len(sentence_with_period) <= chunk_size:
                current_chunk += sentence_with_period
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence_with_period

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        final_chunks: List[str] = []
        for chunk in chunks:
            if len(chunk) > chunk_size:
                for i in range(0, len(chunk), chunk_size):
                    final_chunks.append(chunk[i : i + chunk_size])
            else:
                final_chunks.append(chunk)

        return final_chunks

    async def _generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate a single embedding using Cohere
        """
        try:
            response = await asyncio.to_thread(
                self.cohere.embed,
                texts=[text],
                model=config.EMBEDDING_MODEL,
                input_type="search_document",
            )

            return response.embeddings[0]

        except Exception as e:
            logger.error(f"Error generating single embedding: {e}")
            raise RAGException(f"Error generating embedding: {str(e)}")

    async def get_embeddings_count(self) -> int:
        """
        Get total number of embeddings
        """
        try:
            return await qdrant_service.get_all_embeddings_count()
        except Exception as e:
            logger.error(f"Error getting embeddings count: {e}")
            raise RAGException(f"Error getting embeddings count: {str(e)}")

    async def delete_embeddings_for_chapter(self, chapter_id: str):
        """
        Delete all embeddings for a chapter
        """
        try:
            await qdrant_service.delete_embeddings_by_chapter(chapter_id)
            logger.info(f"Deleted embeddings for chapter {chapter_id}")
        except Exception as e:
            logger.error(
                f"Error deleting embeddings for chapter {chapter_id}: {e}"
            )
            raise RAGException(f"Error deleting embeddings: {str(e)}")


# Global instance
embedding_service = EmbeddingService()
