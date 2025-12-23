# Non-Functional Requirements (Frozen)

This document defines the quality attributes, constraints, and operational characteristics of the system.
No implementation may violate these requirements.

---

## NFR-1: Performance
The system shall provide acceptable response times for all user-facing interactions.

Acceptance Criteria:
- Textbook pages load within 3 seconds on a standard broadband connection
- Chatbot responses are returned within 5 seconds under normal load
- Content personalization does not introduce noticeable latency

---

## NFR-2: Scalability
The system shall support multiple concurrent users.

Acceptance Criteria:
- The chatbot backend supports concurrent user requests
- Vector search performance remains stable as content grows
- The system can scale horizontally if needed

---

## NFR-3: Reliability
The system shall operate reliably under normal conditions.

Acceptance Criteria:
- The system gracefully handles backend failures
- Partial outages (e.g., chatbot unavailable) do not break textbook access
- Errors are logged for debugging purposes

---

## NFR-4: Security
The system shall protect user data and prevent unauthorized access.

Acceptance Criteria:
- Authentication data is securely stored
- API endpoints are protected from unauthorized access
- Sensitive configuration values are not hard-coded in the repository

---

## NFR-5: Maintainability
The system shall be easy to understand and modify.

Acceptance Criteria:
- Code is structured according to the defined architecture
- Each component maps to a documented functional requirement
- Agent and skill definitions are documented and traceable

---

## NFR-6: Portability
The system shall be deployable across environments.

Acceptance Criteria:
- The frontend can be deployed to GitHub Pages or equivalent
- The backend can run in a containerized environment
- Environment-specific configuration is externalized

---

## NFR-7: Usability
The system shall be usable by non-technical learners.

Acceptance Criteria:
- The textbook interface is simple and intuitive
- Chatbot access is clearly visible
- Personalization and translation controls are discoverable

---

## NFR-8: Compliance with Scope
The system shall remain within the defined project scope.

Acceptance Criteria:
- No real robot control is implemented
- No live ROS, Gazebo, or Isaac Sim execution occurs
- The system remains educational and AI-native in focus

---

## Non-Functional Requirements Freeze
These non-functional requirements are final.
Any change must be formally documented and reviewed.
