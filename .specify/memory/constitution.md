<!-- SYNC IMPACT REPORT
Version change: N/A (initial creation) → v1.0.0
Modified principles: N/A (new project)
Added sections: All sections (new constitution)
Removed sections: N/A
Templates requiring updates: N/A (new constitution)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity and Minimalism
All implementations must prioritize simplicity over complexity; features should be minimal and focused; solutions must follow YAGNI principles and avoid over-engineering.

### II. Accuracy and Quality
Content and code examples must be technically accurate and professionally reviewed; all information presented must be factually correct and verified; quality over quantity in all deliverables.

### III. Free-Tier Architecture
All system components must operate within free-tier constraints; no heavy GPU usage or expensive resources allowed; solutions must be cost-effective and accessible.

### IV. Fast Builds and Deployments
All build processes must complete efficiently; deployment to GitHub Pages must be smooth and reliable; performance considerations must guide all implementation choices.

### V. RAG-Only Information Source
The chatbot must provide answers solely from book text content; no external information sources allowed; RAG system must be properly configured to reference only textbook materials.

### VI. Clean UI/UX Experience
Docusaurus interface must be clean, intuitive, and professional; user experience should be seamless across all features; visual design should enhance learning experience.

## Technical Requirements

### Chapter Structure
The textbook must contain exactly 6 short chapters covering: Introduction to Physical AI, Basics of Humanoid Robotics, ROS 2 Fundamentals, Digital Twin Simulation (Gazebo + Isaac), Vision-Language-Action Systems, and Capstone: Simple AI-Robot Pipeline.

### Technology Stack
Must use Docusaurus for textbook UI, Qdrant for vector storage, Neon for database, FastAPI for backend services, with RAG chatbot functionality and select-text → Ask AI feature. Optional Urdu/personalization features may be implemented.

### Performance Constraints
Embeddings must be lightweight and efficient; no resource-intensive operations that exceed free-tier limitations; all components must perform adequately within budget constraints.

## Development Workflow

### Implementation Approach
Features must be developed incrementally with clear acceptance criteria; testing should validate both functionality and performance within free-tier limits; code reviews must verify adherence to principles.

### Quality Assurance
All features must be tested for accuracy and performance; deployment must be verified on GitHub Pages; chatbot functionality must be validated against textbook content.

### Documentation Standards
All code must be documented with clear explanations; user guides must be provided for all features; setup and deployment instructions must be comprehensive.

## Governance

This constitution serves as the governing document for all development activities. All team members must adhere to these principles and requirements. Changes to this constitution require explicit approval and documentation of the rationale. All implementations, code reviews, and deployments must be evaluated against these principles.

**Version**: v1.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19