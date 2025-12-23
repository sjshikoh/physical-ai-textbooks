# Functional Requirements (Frozen)

This document defines the functional capabilities the system must provide.
No functionality may be added without updating this document.

---

## FR-1: Textbook Hosting
The system shall host a web-based textbook for the Physical AI & Humanoid Robotics course.

Acceptance Criteria:
- Content is organized into modules and chapters
- The textbook is accessible via a web browser
- Navigation (sidebar, next/previous) is available

---

## FR-2: AI-Assisted Content Authoring
The system shall support AI-assisted creation and refinement of textbook content.

Acceptance Criteria:
- AI agents can generate or refine content
- Generated content aligns with the defined course outline
- Content is stored in Markdown format

---

## FR-3: Embedded RAG Chatbot
The system shall provide an embedded Retrieval-Augmented Generation (RAG) chatbot to answer user questions.

Acceptance Criteria:
- The chatbot answers only using indexed textbook content
- The chatbot does not use external or general knowledge
- The chatbot can answer questions based on user-selected text

---

## FR-4: Content Ingestion and Indexing
The system shall ingest textbook content into a vector database for semantic retrieval.

Acceptance Criteria:
- Each chapter and section is embedded
- Content is retrievable via semantic search
- The ingestion process is reproducible

---

## FR-5: User Authentication
The system shall provide user signup and signin functionality.

Acceptance Criteria:
- Signup collects the user's software and hardware background
- Authenticated sessions are maintained
- Anonymous users have limited access

---

## FR-6: Content Personalization
The system shall personalize content for authenticated users.

Acceptance Criteria:
- Content adapts based on the user's background
- Users can switch between beginner and advanced explanations
- Personalization is user-controlled

---

## FR-7: Urdu Translation
The system shall allow users to translate chapter content into Urdu.

Acceptance Criteria:
- Translation occurs on user request
- Technical meaning is preserved
- Original English content remains unchanged

---

## FR-8: Public Deployment
The system shall be publicly accessible.

Acceptance Criteria:
- The textbook is deployed on GitHub Pages or an equivalent platform
- A public URL is available
- No local setup is required for access

---

## Functional Requirements Freeze
These functional requirements are final.
No additional features may be introduced without formally updating this document.
