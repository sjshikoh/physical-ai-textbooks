---
id: 1
title: Create Physical AI Constitution
stage: constitution
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: shaista
command: /sp.constitution
labels: [constitution,physical-ai,humanoid-robotics,docusaurus,rag]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course.
The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI
and a fully integrated free-tier RAG chatbot.

Scope:
- 6 short chapters:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Clean UI
- Free-tier friendly
- Lightweight embeddings

Core Principles:
- Simplicity
- Accuracy
- Minimalism
- Fast builds
- Free-tier architecture
- RAG answers ONLY from book text

Key Features:
- Docusaurus textbook
- RAG chatbot (Qdrant + Neon + FastAPI)
- Select-text → Ask AI
- Optional Urdu / Personalize features

Constraints:
- No heavy GPU usage
- Minimal embeddings

Success Criteria:
- Build success
- Accurate chatbot
- Clean UI
- Smooth GitHub Pages deployment

Generate full constitution.

## Response snapshot

Created the constitution for the Physical AI & Humanoid Robotics textbook project with the following key elements:

1. Core Principles:
   - Simplicity and Minimalism
   - Accuracy and Quality
   - Free-Tier Architecture
   - Fast Builds and Deployments
   - RAG-Only Information Source
   - Clean UI/UX Experience

2. Technical Requirements:
   - Chapter Structure (6 required chapters)
   - Technology Stack (Docusaurus, Qdrant, Neon, FastAPI)
   - Performance Constraints (lightweight, free-tier)

3. Development Workflow:
   - Implementation Approach
   - Quality Assurance
   - Documentation Standards

4. Governance section with version tracking

## Outcome

- ✅ Impact: Created initial project constitution document at .specify/memory/constitution.md with all specified principles and requirements
- 🧪 Tests: none
- 📁 Files: 1 file created (.specify/memory/constitution.md)
- 🔁 Next prompts: Proceed with project implementation based on constitution
- 🧠 Reflection: Constitution successfully captures all key requirements from user input and establishes governance structure for the project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing textbook structure based on constitution