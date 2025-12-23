# Agent Skills Specification

This document defines the reusable skills available to AI agents in the system.
Skills represent capabilities, not implementations.

---

## Skill 1: Educational Content Generation

### Description
Ability to generate structured, educational content aligned with defined learning objectives.

### Inputs
- Course outline
- Chapter intent
- Target learner level

### Outputs
- Markdown-formatted educational content

### Constraints
- Content must remain within the approved course scope
- Tone must be instructional and neutral

---

## Skill 2: Curriculum Flow Reasoning

### Description
Ability to reason about logical progression between topics.

### Inputs
- Module and chapter structure
- Learning objectives

### Outputs
- Validation of topic sequencing
- Recommendations for ordering

### Constraints
- Cannot introduce new topics outside the course outline

---

## Skill 3: Semantic Content Chunking

### Description
Ability to segment textbook content into retrievable semantic units.

### Inputs
- Markdown chapters
- Section boundaries

### Outputs
- Content chunks suitable for retrieval

### Constraints
- Must preserve contextual coherence
- Cannot alter original content meaning

---

## Skill 4: Grounded Question Answering

### Description
Ability to answer user questions using only retrieved content.

### Inputs
- User question
- Retrieved content segments
- Optional user-selected text

### Outputs
- Context-grounded answer

### Constraints
- No external or general knowledge usage
- Answers must be traceable to retrieved content

---

## Skill 5: User Background Interpretation

### Description
Ability to interpret user background data for personalization.

### Inputs
- User-provided background information

### Outputs
- Personalization parameters (e.g., explanation depth)

### Constraints
- Cannot modify canonical content
- Must respect user privacy

---

## Skill 6: Educational Content Adaptation

### Description
Ability to adapt explanation depth without changing meaning.

### Inputs
- Original content
- Personalization parameters

### Outputs
- Adapted content variant

### Constraints
- Core technical meaning must remain unchanged

---

## Skill 7: Technical Translation (English to Urdu)

### Description
Ability to translate educational content from English to Urdu.

### Inputs
- English textbook content

### Outputs
- Urdu-translated content

### Constraints
- Technical terminology accuracy must be preserved
- Translation must not overwrite original content
