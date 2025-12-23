from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from ..services.textbook_service import textbook_service
from ..utils.database import get_db_session
from ..models.chapter import Chapter
from ..utils.logging import get_logger, TextbookException

logger = get_logger(__name__)
router = APIRouter(prefix="/textbook", tags=["Textbook"])

@router.get("/chapters", summary="Get all textbook chapters")
async def get_all_chapters(
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Retrieve a list of all textbook chapters with their metadata
    """
    try:
        chapters = await textbook_service.get_all_chapters(db)
        return {
            "chapters": [chapter.model_dump() for chapter in chapters],
            "total": len(chapters)
        }
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error getting all chapters: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error occurred while retrieving chapters"}
        )


@router.get("/chapters/{slug}", summary="Get a specific chapter")
async def get_chapter_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Retrieve a textbook chapter by its slug
    """
    try:
        chapter = await textbook_service.get_chapter_by_slug(db, slug)
        if not chapter:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Chapter with slug '{slug}' not found"}
            )

        return {"chapter": chapter.model_dump()}
    except HTTPException:
        raise
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error getting chapter {slug}: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Internal server error occurred while retrieving chapter {slug}"}
        )


@router.post("/chapters", summary="Create a new textbook chapter")
async def create_chapter(
    chapter_data: Chapter,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Create a new textbook chapter
    """
    try:
        # Use ChapterCreate model for validation
        chapter_create = chapter_data  # This will be validated by Pydantic
        new_chapter = await textbook_service.create_chapter(db, chapter_create)
        return {"chapter": new_chapter.model_dump()}
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error creating chapter: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error occurred while creating chapter"}
        )


@router.put("/chapters/{slug}", summary="Update an existing textbook chapter")
async def update_chapter(
    slug: str,
    chapter_data: Chapter,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Update an existing textbook chapter
    """
    try:
        # Use ChapterUpdate model for validation
        from ..models.chapter import ChapterUpdate
        chapter_update = ChapterUpdate(
            title=chapter_data.title,
            content=chapter_data.content,
            order=chapter_data.order,
            metadata=chapter_data.metadata
        )
        updated_chapter = await textbook_service.update_chapter(db, slug, chapter_update)
        if not updated_chapter:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Chapter with slug '{slug}' not found"}
            )

        return {"chapter": updated_chapter.model_dump()}
    except HTTPException:
        raise
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error updating chapter {slug}: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Internal server error occurred while updating chapter {slug}"}
        )


@router.delete("/chapters/{slug}", summary="Delete a textbook chapter")
async def delete_chapter(
    slug: str,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Delete a textbook chapter
    """
    try:
        success = await textbook_service.delete_chapter(db, slug)
        if not success:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Chapter with slug '{slug}' not found"}
            )

        return {"message": f"Chapter with slug '{slug}' deleted successfully"}
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting chapter {slug}: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Internal server error occurred while deleting chapter {slug}"}
        )


@router.post("/chapters/{slug}/embeddings", summary="Generate embeddings for a chapter")
async def generate_chapter_embeddings(
    slug: str,
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Generate and store embeddings for a specific chapter
    """
    try:
        success = await textbook_service.generate_embeddings_for_chapter(db, slug)
        if not success:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Chapter with slug '{slug}' not found"}
            )

        return {"message": f"Embeddings generated for chapter with slug '{slug}' successfully"}
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error generating embeddings for chapter {slug}: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Internal server error occurred while generating embeddings for chapter {slug}"}
        )


@router.post("/chapters/load-from-content", summary="Load chapters from content directory")
async def load_chapters_from_content(
    content_dir: str = "frontend/docs",  # Default to frontend/docs
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Load textbook chapters from content directory and save to database
    """
    try:
        chapters = await textbook_service.load_chapters_from_content(db, content_dir)
        return {
            "chapters": [chapter.model_dump() for chapter in chapters],
            "total": len(chapters),
            "message": f"Successfully loaded {len(chapters)} chapters from content directory"
        }
    except TextbookException as e:
        logger.error(f"Textbook error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error loading chapters from content: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error occurred while loading chapters from content"}
        )


@router.get("/health", summary="Check textbook service health")
async def textbook_health_check(
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Check if the textbook service is available and responding
    """
    try:
        # Try to get the count of chapters as a basic health check
        chapters = await textbook_service.get_all_chapters(db)

        return {
            "status": "healthy",
            "message": f"Textbook service is operational with {len(chapters)} chapters",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Textbook health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Textbook service has issues: {str(e)}",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }