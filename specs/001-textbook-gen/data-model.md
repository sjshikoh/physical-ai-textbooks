# Data Model: AI-Native Textbook with RAG Chatbot

## Core Entities

### Textbook Chapter
- **id**: string (UUID) - Unique identifier for the chapter
- **title**: string - Title of the chapter
- **slug**: string - URL-friendly identifier
- **content**: string - Markdown content of the chapter
- **order**: integer - Position in the textbook sequence (1-6)
- **created_at**: datetime - Timestamp of creation
- **updated_at**: datetime - Timestamp of last update
- **metadata**: JSON - Additional chapter metadata

### Embedding Vector
- **id**: string (UUID) - Unique identifier for the embedding
- **chapter_id**: string (UUID) - Reference to the chapter
- **text_content**: string - The original text that was embedded
- **vector**: array<float> - The embedding vector (varies by model)
- **chunk_index**: integer - Position of this chunk within the chapter
- **created_at**: datetime - Timestamp of embedding creation

### User Session
- **id**: string (UUID) - Unique identifier for the session
- **user_id**: string (optional) - Identifier for authenticated users
- **session_token**: string - Session identifier for anonymous users
- **created_at**: datetime - Timestamp of session start
- **last_activity**: datetime - Timestamp of last activity
- **preferences**: JSON - User preferences and personalization settings

### RAG Query
- **id**: string (UUID) - Unique identifier for the query
- **session_id**: string (UUID) - Reference to the user session
- **query_text**: string - Original user query
- **response_text**: string - AI-generated response
- **source_chunks**: array<string> - IDs of source chunks used for response
- **confidence_score**: float - Confidence score of the response (0-1)
- **created_at**: datetime - Timestamp of query
- **query_type**: string - Type of query (general, text-selection, etc.)

### User Preference (Optional)
- **id**: string (UUID) - Unique identifier
- **session_id**: string (UUID) - Reference to the session
- **preference_key**: string - Key for the preference
- **preference_value**: string - Value of the preference
- **created_at**: datetime - Timestamp of creation
- **updated_at**: datetime - Timestamp of last update

## Relationships

```
Textbook Chapter (1) ←→ (N) Embedding Vector
    chapter_id ←→ chapter_id

User Session (1) ←→ (N) RAG Query
    session_id ←→ session_id

User Session (1) ←→ (N) User Preference
    session_id ←→ session_id

RAG Query (1) ←→ (N) Embedding Vector (via source_chunks)
    source_chunks → embedding vector IDs
```

## Validation Rules

### Textbook Chapter
- Title must be 1-200 characters
- Slug must be unique and URL-friendly
- Order must be between 1-6
- Content must not be empty

### Embedding Vector
- chapter_id must reference an existing chapter
- text_content must be non-empty
- vector must have consistent dimensions
- chunk_index must be non-negative

### RAG Query
- query_text must be 1-1000 characters
- confidence_score must be between 0-1
- session_id must reference an existing session

## State Transitions

### User Session
- **Active**: When first created and user is interacting
- **Inactive**: After period of inactivity (for cleanup purposes)

## Indexes

### Performance-critical indexes
- Textbook Chapter: `slug` (unique), `order`
- Embedding Vector: `chapter_id`, `chunk_index`
- RAG Query: `session_id`, `created_at`
- User Session: `session_token`, `last_activity`

## Constraints

- Each chapter must have unique order within the textbook
- Embedding vectors must reference valid chapters
- RAG queries must be associated with valid sessions
- Content integrity: textbook content should not be modified without proper versioning