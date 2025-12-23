# AI Agents Specification

This document defines the AI agents used in the Physical AI & Humanoid Robotics textbook system.
Each agent has a clearly defined responsibility and operates strictly within scope.

---

## Agent 1: Content Authoring Agent

### Purpose
To generate and refine educational content for the Physical AI & Humanoid Robotics textbook.

### Responsibilities
- Create structured textbook content based on the approved course outline
- Explain technical concepts in a clear, educational manner
- Maintain consistency in terminology and style across chapters

### Out of Scope
- Making architectural or system design decisions
- Referencing content outside the approved course scope

---

## Agent 2: Curriculum Structuring Agent

### Purpose
To ensure the textbook content follows a coherent educational progression.

### Responsibilities
- Organize chapters and modules according to learning objectives
- Validate logical flow between topics
- Ensure alignment with the defined course structure

### Out of Scope
- Writing full chapter content
- Performing content translation or personalization

---

## Agent 3: Content Ingestion Agent

### Purpose
To prepare textbook content for retrieval and search.

### Responsibilities
- Segment chapters into retrievable units
- Generate vector representations of content
- Store indexed content in the vector database

### Out of Scope
- Answering user questions
- Modifying original textbook content

---

## Agent 4: RAG Answering Agent

### Purpose
To answer user questions using Retrieval-Augmented Generation.

### Responsibilities
- Retrieve relevant textbook content based on user queries
- Generate answers strictly grounded in retrieved content
- Respect user-selected text as contextual input

### Out of Scope
- Using external or general-purpose knowledge
- Answering questions unrelated to the textbook

---

## Agent 5: Personalization Agent

### Purpose
To adapt textbook content based on the user's background.

### Responsibilities
- Interpret user background data collected during signup
- Adjust explanation depth (beginner vs advanced)
- Preserve the original meaning of content during adaptation

### Out of Scope
- Modifying the canonical textbook content
- Persisting personalized content as the default version

---

## Agent 6: Translation Agent

### Purpose
To translate textbook content from English to Urdu.

### Responsibilities
- Translate content on user request
- Preserve technical accuracy and educational intent
- Maintain a neutral and academic tone

### Out of Scope
- Translating user-generated questions
- Replacing the original English content

---

## Agent Scope Enforcement

Each agent operates independently within its defined scope.
No agent may assume responsibilities assigned to another agent.
