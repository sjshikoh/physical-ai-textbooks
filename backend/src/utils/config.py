import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Central configuration class for the Physical AI Textbook RAG backend
    """

    # ==============================
    # Application
    # ==============================
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_V1_STR = "/api/v1"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # ==============================
    # Qdrant Configuration
    # ==============================
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "textbook_embeddings"
    )

    # ==============================
    # Cohere Configuration (FREE TIER)
    # ==============================
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "embed-english-v3.0"
    )

    GENERATION_MODEL = os.getenv(
        "GENERATION_MODEL",
        "command-light"
    )

    # ==============================
    # RAG Configuration
    # ==============================
    RAG_TEMPERATURE = float(os.getenv("RAG_TEMPERATURE", "0.3"))
    RAG_MAX_TOKENS = int(os.getenv("RAG_MAX_TOKENS", "300"))
    RAG_TIMEOUT = int(os.getenv("RAG_TIMEOUT", "30"))  # seconds

    # ==============================
    # Database (Neon)
    # ==============================
    DATABASE_URL = os.getenv(
        "NEON_DATABASE_URL",
        "postgresql://username:password@localhost:5432/textbook_db"
    )

    # ==============================
    # Performance Configuration
    # ==============================
    MAX_CONCURRENT_USERS = int(os.getenv("MAX_CONCURRENT_USERS", "100"))

    # ==============================
    # Textbook Configuration
    # ==============================
    TEXTBOOK_CHAPTERS_COUNT = 6

    # ==============================
    # Validation
    # ==============================
    def validate(self):
        errors = []

        if not self.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is missing")

        if not self.QDRANT_URL:
            errors.append("QDRANT_URL is missing")

        if not self.QDRANT_COLLECTION_NAME:
            errors.append("QDRANT_COLLECTION_NAME is missing")

        if errors:
            raise RuntimeError(
                "Configuration error(s):\n- " + "\n- ".join(errors)
            )


# Create a singleton instance
config = Config()
config.validate()
