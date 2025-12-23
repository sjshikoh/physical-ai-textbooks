---
id: agents
title: AI Agents
sidebar_position: 5
---

## What is an AI Agent?

An **AI Agent** is an autonomous or semi-autonomous system that:
- Perceives information (text, vision, sensor data)
- Reasons over knowledge
- Decides actions
- Executes tasks via tools, APIs, or robots

In this course, agents are **software-first**, designed to later control **physical systems**.

---

## Agents in the Physical AI Textbook

### 1. 📘 Textbook Ingestion Agent
**Purpose:**  
Ingests curriculum content (Markdown, PDFs, Docs) and converts it into embeddings.

**Responsibilities:**
- Load course documents
- Chunk text
- Generate embeddings
- Store vectors in Qdrant

**Backend Mapping:**
- `src/services/textbook_loader.py`
- `src/services/embedding_service.py`

---

### 2. 🔍 Retrieval Agent (RAG)
**Purpose:**  
Finds relevant knowledge chunks for a user query.

**Responsibilities:**
- Convert query → embedding
- Perform vector similarity search
- Rank results

**Backend Mapping:**
- `src/services/rag_service.py`
- `src/utils/qdrant_client.py`

---

### 3. 🧠 Reasoning Agent
**Purpose:**  
Synthesizes retrieved knowledge into a coherent answer.

**Responsibilities:**
- Combine retrieved context
- Call LLM (Cohere)
- Control temperature & max tokens

**Backend Mapping:**
- `src/services/llm_service.py`

---

### 4. 🧑‍🏫 Tutor Agent
**Purpose:**  
Explains concepts step-by-step for learning.

**Capabilities:**
- Beginner-friendly explanations
- Examples
- Concept breakdowns

---

### 5. 🤖 Physical AI Extension (Future)
**Purpose:**  
Bridge software intelligence to humanoid robots.

**Examples:**
- Task planning
- Motion planning
- Sensor feedback loops

---

## Agent Design Principles
- Modular
- Tool-augmented
- Model-agnostic
- Hardware-ready

---

## Summary
Agents are the **core abstraction** connecting:
**Knowledge → Reasoning → Action → Physical Systems**
