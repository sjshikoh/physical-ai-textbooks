from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.chapter import Chapter, ChapterCreate, ChapterUpdate
from ..utils.logging import get_logger, TextbookException
from ..utils.textbook_loader import textbook_loader
from ..services.embedding_service import embedding_service
import logging

logger = get_logger(__name__)

class TextbookService:
    """
    Service class for handling textbook-related operations
    """

    async def get_all_chapters(self, db: AsyncSession) -> List[Chapter]:
        """
        Get all textbook chapters

        Args:
            db: Database session

        Returns:
            List of all chapters
        """
        try:
            result = await db.execute(
                select(Chapter)
                .order_by(Chapter.order)
            )
            chapters = result.scalars().all()
            logger.info(f"Retrieved {len(chapters)} chapters from database")
            return [Chapter.model_validate(chapter) for chapter in chapters]
        except Exception as e:
            logger.error(f"Error retrieving chapters: {e}")
            raise TextbookException(f"Error retrieving chapters: {str(e)}")

    async def get_chapter_by_slug(self, db: AsyncSession, slug: str) -> Optional[Chapter]:
        """
        Get a textbook chapter by its slug

        Args:
            db: Database session
            slug: Chapter slug

        Returns:
            Chapter object or None if not found
        """
        try:
            result = await db.execute(
                select(Chapter)
                .where(Chapter.slug == slug)
            )
            chapter = result.scalar_one_or_none()
            if chapter:
                logger.info(f"Retrieved chapter with slug: {slug}")
                return Chapter.model_validate(chapter)
            else:
                logger.warning(f"Chapter with slug {slug} not found")
                return None
        except Exception as e:
            logger.error(f"Error retrieving chapter with slug {slug}: {e}")
            raise TextbookException(f"Error retrieving chapter: {str(e)}")

    async def create_chapter(self, db: AsyncSession, chapter_data: ChapterCreate) -> Chapter:
        """
        Create a new textbook chapter

        Args:
            db: Database session
            chapter_data: Chapter creation data

        Returns:
            Created chapter object
        """
        try:
            # Check if slug already exists
            existing_chapter = await self.get_chapter_by_slug(db, chapter_data.slug)
            if existing_chapter:
                raise TextbookException(f"Chapter with slug {chapter_data.slug} already exists")

            # Create new chapter
            chapter = Chapter(**chapter_data.model_dump())

            # Add to database
            db.add(chapter)
            await db.commit()
            await db.refresh(chapter)

            logger.info(f"Created chapter with slug: {chapter.slug}")
            return Chapter.model_validate(chapter)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating chapter: {e}")
            raise TextbookException(f"Error creating chapter: {str(e)}")

    async def update_chapter(self, db: AsyncSession, slug: str, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """
        Update an existing textbook chapter

        Args:
            db: Database session
            slug: Chapter slug
            chapter_data: Chapter update data

        Returns:
            Updated chapter object or None if not found
        """
        try:
            # Get existing chapter
            chapter = await self.get_chapter_by_slug(db, slug)
            if not chapter:
                logger.warning(f"Chapter with slug {slug} not found for update")
                return None

            # Prepare update data
            update_data = chapter_data.model_dump(exclude_unset=True)

            # Update chapter fields
            for field, value in update_data.items():
                setattr(chapter, field, value)

            # Commit changes
            await db.commit()
            await db.refresh(chapter)

            logger.info(f"Updated chapter with slug: {slug}")
            return Chapter.model_validate(chapter)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating chapter with slug {slug}: {e}")
            raise TextbookException(f"Error updating chapter: {str(e)}")

    async def delete_chapter(self, db: AsyncSession, slug: str) -> bool:
        """
        Delete a textbook chapter

        Args:
            db: Database session
            slug: Chapter slug

        Returns:
            True if chapter was deleted, False if not found
        """
        try:
            # Get existing chapter
            chapter = await self.get_chapter_by_slug(db, slug)
            if not chapter:
                logger.warning(f"Chapter with slug {slug} not found for deletion")
                return False

            # Delete from database
            await db.delete(chapter)
            await db.commit()

            logger.info(f"Deleted chapter with slug: {slug}")
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting chapter with slug {slug}: {e}")
            raise TextbookException(f"Error deleting chapter: {str(e)}")

    async def load_chapters_from_content(self, db: AsyncSession, content_dir: str = "frontend/docs") -> List[Chapter]:
        """
        Load textbook chapters from content directory and save to database

        Args:
            db: Database session
            content_dir: Directory where textbook content is stored

        Returns:
            List of loaded chapters
        """
        try:
            # Load chapters from content directory
            chapter_data_list = textbook_loader.load_chapters_from_directory()

            loaded_chapters = []
            for chapter_data in chapter_data_list:
                # Create or update chapter in database
                existing_chapter = await self.get_chapter_by_slug(db, chapter_data['slug'])

                if existing_chapter:
                    # Update existing chapter
                    chapter_update = ChapterUpdate(
                        title=chapter_data['title'],
                        content=chapter_data['content'],
                        order=chapter_data['order'],
                        metadata=chapter_data['metadata']
                    )
                    updated_chapter = await self.update_chapter(db, chapter_data['slug'], chapter_update)
                    loaded_chapters.append(updated_chapter)
                else:
                    # Create new chapter
                    chapter_create = ChapterCreate(
                        title=chapter_data['title'],
                        slug=chapter_data['slug'],
                        content=chapter_data['content'],
                        order=chapter_data['order'],
                        metadata=chapter_data['metadata']
                    )
                    new_chapter = await self.create_chapter(db, chapter_create)
                    loaded_chapters.append(new_chapter)

            logger.info(f"Loaded {len(loaded_chapters)} chapters from content directory")
            return loaded_chapters
        except Exception as e:
            logger.error(f"Error loading chapters from content directory: {e}")
            raise TextbookException(f"Error loading chapters from content: {str(e)}")

    async def generate_embeddings_for_chapter(self, db: AsyncSession, slug: str) -> bool:
        """
        Generate and store embeddings for a specific chapter

        Args:
            db: Database session
            slug: Chapter slug

        Returns:
            True if embeddings were generated successfully, False otherwise
        """
        try:
            # Get the chapter
            chapter = await self.get_chapter_by_slug(db, slug)
            if not chapter:
                logger.warning(f"Chapter with slug {slug} not found for embedding generation")
                return False

            # Generate and store embeddings
            await embedding_service.store_chapter_embeddings(chapter.id, chapter.content)

            logger.info(f"Generated embeddings for chapter with slug: {slug}")
            return True
        except Exception as e:
            logger.error(f"Error generating embeddings for chapter {slug}: {e}")
            raise TextbookException(f"Error generating embeddings for chapter: {str(e)}")

    async def generate_embeddings_for_all_chapters(self, db: AsyncSession) -> Dict[str, bool]:
        """
        Generate and store embeddings for all chapters

        Args:
            db: Database session

        Returns:
            Dictionary mapping chapter slugs to success status
        """
        try:
            # Get all chapters
            chapters = await self.get_all_chapters(db)

            results = {}
            for chapter in chapters:
                try:
                    # Generate embeddings for this chapter
                    success = await self.generate_embeddings_for_chapter(db, chapter.slug)
                    results[chapter.slug] = success
                except Exception as e:
                    logger.error(f"Error generating embeddings for chapter {chapter.slug}: {e}")
                    results[chapter.slug] = False

            logger.info(f"Completed embedding generation for {len(chapters)} chapters")
            return results
        except Exception as e:
            logger.error(f"Error generating embeddings for all chapters: {e}")
            raise TextbookException(f"Error generating embeddings for all chapters: {str(e)}")


# Global instance
textbook_service = TextbookService()