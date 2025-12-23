import os
import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path
from ..models.chapter import Chapter, ChapterCreate
import logging

logger = logging.getLogger(__name__)


class TextbookLoader:
    """
    Service class for loading textbook content from various sources
    """

    def __init__(self, content_dir: Optional[str] = None):
        """
        Initialize the textbook loader

        Args:
            content_dir: Directory where textbook content is stored
        """

        # Resolve project root safely:
        # backend/src/utils/textbook_loader.py -> parents[3] = project root
        BASE_DIR = Path(__file__).resolve().parents[3]

        # Default to Docusaurus docs directory
        DEFAULT_DOCS_DIR = BASE_DIR / "website" / "docs"

        self.content_dir = Path(content_dir) if content_dir else DEFAULT_DOCS_DIR

        logger.info(f"Looking for textbook content in: {self.content_dir}")
        logger.info(f"Content directory exists: {self.content_dir.exists()}")

        if not self.content_dir.exists():
            logger.warning(f"Content directory {self.content_dir} does not exist")

    def load_chapters_from_directory(self) -> List[Dict[str, Any]]:
        """
        Load textbook chapters from the content directory

        Returns:
            List of chapter dictionaries
        """
        chapters: List[Dict[str, Any]] = []

        if not self.content_dir.exists():
            logger.warning(
                f"Content directory {self.content_dir} does not exist, returning empty list"
            )
            return chapters

        # Look for markdown files (top-level only)
        for file_path in self.content_dir.glob("*.md"):
            if self._is_chapter_file(file_path.name):
                try:
                    chapter_data = self._load_chapter_from_file(file_path)
                    if chapter_data:
                        chapters.append(chapter_data)
                except Exception as e:
                    logger.error(f"Error loading chapter from {file_path}: {e}")

        # Sort chapters by order
        chapters.sort(key=lambda x: x.get("order", 0))

        logger.info(f"Loaded {len(chapters)} chapters from {self.content_dir}")
        return chapters

    def _is_chapter_file(self, filename: str) -> bool:
        """
        Check if a file is a textbook chapter file

        Args:
            filename: Name of the file to check

        Returns:
            True if the file is a chapter file, False otherwise
        """
        # Chapter files typically start with a number followed by a dash
        # e.g., 01-intro-to-physical-ai.md
        import re

        pattern = r"^\d{2,}-.*\.md$"
        return bool(re.match(pattern, filename))

    def _load_chapter_from_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single chapter from a markdown file

        Args:
            file_path: Path to the markdown file

        Returns:
            Chapter data dictionary or None if loading failed
        """
        with open(file_path, "r", encoding="utf-8") as file:
            raw_content = file.read()

        # Extract metadata and content
        metadata, content = self._extract_metadata_and_content(
            raw_content, file_path.name
        )

        # Generate slug from filename
        slug = file_path.stem

        # Extract order from filename (leading digits)
        import re

        match = re.match(r"^(\d{2,})-", file_path.name)
        order = int(match.group(1)) if match else 0

        # Determine title
        title = (
            metadata.get("title")
            or self._extract_title_from_content(content)
            or slug.replace("-", " ").title()
        )

        chapter_data = {
            "id": None,  # Generated when saved to DB
            "title": title,
            "slug": slug,
            "content": content,
            "order": order,
            "metadata": metadata,
            "created_at": None,
            "updated_at": None,
        }

        return chapter_data

    def _extract_metadata_and_content(
        self, content: str, filename: str
    ) -> tuple[Dict[str, Any], str]:
        """
        Extract YAML frontmatter metadata from content if present

        Args:
            content: Raw markdown content
            filename: Name of the file being processed

        Returns:
            Tuple of (metadata dict, content without metadata)
        """
        metadata: Dict[str, Any] = {}

        # YAML frontmatter handling
        if content.strip().startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    metadata_yaml = parts[1].strip()
                    content = parts[2].strip()
                    metadata = yaml.safe_load(metadata_yaml) or {}
            except yaml.YAMLError as e:
                logger.warning(
                    f"Error parsing YAML frontmatter in {filename}: {e}"
                )

        return metadata, content

    def _extract_title_from_content(self, content: str) -> Optional[str]:
        """
        Extract title from the first H1 heading

        Args:
            content: Markdown content

        Returns:
            Title string or None
        """
        for line in content.split("\n"):
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
        return None


# Global instance
textbook_loader = TextbookLoader()
