---
id: skills
title: Skills
sidebar_position: 6
---

## What is a Skill?

A **Skill** is a reusable capability that an agent can invoke.

> Agents decide **what** to do.  
> Skills define **how** it is done.

---

## Core Skills in This Project

### 🧠 Embedding Skill
**Description:**  
Converts text into dense vector representations.

**Used by:**
- Ingestion Agent
- Retrieval Agent

**Tech:**
- Cohere Embeddings
- 1536-dimension vectors

---

### 🔎 Vector Search Skill
**Description:**  
Performs semantic similarity search.

**Tech:**
- Qdrant
- Cosine similarity

---

### ✍️ Generation Skill
**Description:**  
Generates natural language responses.

**Tech:**
- Cohere LLM
- Controlled temperature and token limits

---

### 🧩 Chunking Skill
**Description:**  
Splits long documents into manageable pieces.

**Strategies:**
- Fixed-size chunks
- Overlapping windows

---

### 🧪 Validation Skill
**Description:**  
Validates configuration, environment variables, and model compatibility.

**Example:**
- Embedding dimension mismatch detection

---

## Skill Reusability
Skills are:
- Stateless
- Composable
- Agent-agnostic

This allows:
- Rapid experimentation
- Future robotics integration

---

## Summary
Skills are the **building blocks** that power intelligent agents.
