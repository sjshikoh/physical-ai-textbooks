from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from .config import config
import logging
import uuid

logger = logging.getLogger(__name__)

class QdrantService:
    """
    Service class for handling Qdrant vector database operations
    """

    def __init__(self):
        self.client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            prefer_grpc=False
        )


        self.collection_name = config.QDRANT_COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the collection exists with the proper configuration
        (SAFE for Qdrant Cloud + newer configs)
        """
        collections_response = self.client.get_collections()
        existing_collections = [c.name for c in collections_response.collections]

        if self.collection_name in existing_collections:
            logger.info(f"Collection '{self.collection_name}' already exists")
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE,
            ),
        )

        logger.info(f"Created collection '{self.collection_name}'")

    async def store_embeddings(self, chapter_id: str, embeddings_data: List[Dict[str, Any]]):
        """
        Store embeddings for a chapter in Qdrant

        Args:
            chapter_id: ID of the chapter
            embeddings_data: List of dictionaries containing text_content and vector
        """
        points = []
        for idx, data in enumerate(embeddings_data):
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=data["vector"],
                    payload={
                        "chapter_id": chapter_id,
                        "text_content": data["text_content"],
                        "chunk_index": idx
                    }
                )
            )

        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Stored {len(points)} embeddings for chapter {chapter_id}")

    async def search_similar(self, query_vector: List[float], chapter_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings to the query vector

        Args:
            query_vector: The embedding vector to search for
            chapter_id: Optional chapter ID to limit search to specific chapter
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing text_content and similarity score
        """
        # Prepare filters
        filters = []
        if chapter_id:
            filters.append(
                models.FieldCondition(
                    key="payload.chapter_id",
                    match=models.MatchValue(value=chapter_id)
                )
            )

        filter_obj = models.Filter(must=filters) if filters else None

        # Perform search
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=filter_obj,
            limit=limit
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                "text_content": result.payload["text_content"],
                "similarity_score": result.score,
                "chapter_id": result.payload["chapter_id"],
                "chunk_index": result.payload["chunk_index"]
            })

        logger.info(f"Found {len(results)} similar embeddings for query")
        return results

    async def delete_embeddings_by_chapter(self, chapter_id: str):
        """
        Delete all embeddings associated with a specific chapter

        Args:
            chapter_id: ID of the chapter whose embeddings to delete
        """
        # Find all points with this chapter_id
        filter_condition = models.Filter(
            must=[
                models.FieldCondition(
                    key="payload.chapter_id",
                    match=models.MatchValue(value=chapter_id)
                )
            ]
        )

        # Delete points
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=filter_condition
            )
        )

        logger.info(f"Deleted embeddings for chapter {chapter_id}")

    async def get_all_embeddings_count(self) -> int:
        """
        Get the total count of embeddings in the collection

        Returns:
            Total number of embeddings
        """
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count

# Global instance
qdrant_service = QdrantService()