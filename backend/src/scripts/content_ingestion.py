#!/usr/bin/env python3
"""
Content Ingestion Script for Physical AI & Humanoid Robotics Textbook

Reads markdown files from the Docusaurus website/docs/ directory,
extracts clean text content, generates embeddings via embedding_service,
and stores them in Qdrant asynchronously.
"""

import os
import re
import logging
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Absolute imports (ensure backend/src is in PYTHONPATH)
from src.services.embedding_service import embedding_service
from src.utils.qdrant_client import qdrant_service
from src.utils.config import config


def extract_frontmatter(content: str) -> Tuple[str, Dict[str, Any]]:
    """Extract frontmatter from markdown content and return remaining content."""
    if content.startswith("---"):
        lines = content.split("\n")
        frontmatter_end = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                frontmatter_end = i
                break

        if frontmatter_end != -1:
            frontmatter_content = "\n".join(lines[1:frontmatter_end])
            remaining_content = "\n".join(lines[frontmatter_end + 1:])
            frontmatter = {}
            for line in frontmatter_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
            return remaining_content.strip(), frontmatter
    return content, {}


def extract_headings(content: str) -> List[Tuple[str, str]]:
    """Extract headings and their associated content from markdown."""
    lines = content.split("\n")
    sections = []
    current_heading = "Introduction"
    current_content = []

    for line in lines:
        if line.strip().startswith("#"):
            if current_content:
                sections.append((current_heading, "\n".join(current_content).strip()))
            current_heading = line.strip().lstrip("#").strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections.append((current_heading, "\n".join(current_content).strip()))

    return sections


def clean_markdown_content(content: str) -> str:
    """Remove markdown formatting and return clean text."""
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'\*(.*?)\*', r'\1', content)
    content = re.sub(r'__(.*?)__', r'\1', content)
    content = re.sub(r'_(.*?)_', r'\1', content)
    content = re.sub(r'```[\s\S]*?```', '', content)
    content = re.sub(r'`(.*?)`', r'\1', content)
    content = re.sub(r'\n\s*\n', '\n\n', content)
    return content.strip()


def process_markdown_file(file_path: Path) -> List[Dict[str, Any]]:
    """Process a single markdown file and return sections ready for embedding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        content_without_frontmatter, frontmatter = extract_frontmatter(raw_content)
        sections = extract_headings(content_without_frontmatter)

        processed_data = []
        for heading, section_content in sections:
            clean_content = clean_markdown_content(section_content)
            if clean_content.strip():
                processed_data.append({
                    "text_content": clean_content,
                    "document_title": frontmatter.get("title", file_path.stem),
                    "file_path": str(file_path),
                    "section_heading": heading
                })

        logger.info(f"Processed {len(processed_data)} sections from {file_path}")
        return processed_data

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return []


async def ingest_content(docs_path: str):
    """Ingest markdown content into Qdrant asynchronously."""
    docs_dir = Path(docs_path)
    if not docs_dir.exists():
        logger.error(f"Docs directory does not exist: {docs_path}")
        return

    markdown_files = list(docs_dir.rglob("*.md"))
    logger.info(f"Found {len(markdown_files)} markdown files to process")

    total_chunks = 0
    processed_files = 0

    for md_file in markdown_files:
        logger.info(f"Processing file: {md_file}")
        content_sections = process_markdown_file(md_file)

        for section in content_sections:
            try:
                chapter_id = f"{section['file_path']}#{section['section_heading']}"

                # Async generate embeddings
                embedding_data = await embedding_service.generate_embeddings_for_chapter(
                    chapter_id=chapter_id,
                    content=section["text_content"],
                    chunk_size=1000
                )

                # Async store embeddings
                await embedding_service.store_chapter_embeddings(
                    chapter_id=chapter_id,
                    content=section["text_content"],
                    chunk_size=1000
                )

                total_chunks += len(embedding_data)

            except Exception as e:
                logger.error(f"Error storing embeddings for {md_file} section '{section['section_heading']}': {e}")

        processed_files += 1

    logger.info(f"Content ingestion completed. Processed {processed_files} files with {total_chunks} chunks.")


async def main():
    """Main entry point for ingestion."""
    # Adjust path to actual docs folder outside backend
    project_root = Path(__file__).parent.parent.parent
    docs_path = project_root / "website" / "docs"

    logger.info(f"Starting content ingestion from: {docs_path}")

    try:
        count = await qdrant_service.get_all_embeddings_count()
        logger.info(f"Current embeddings in Qdrant: {count}")
    except Exception as e:
        logger.error(f"Could not connect to Qdrant: {e}")
        return

    await ingest_content(str(docs_path))

    try:
        final_count = await qdrant_service.get_all_embeddings_count()
        logger.info(f"Final embeddings in Qdrant: {final_count}")
    except Exception as e:
        logger.error(f"Could not get final count from Qdrant: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
