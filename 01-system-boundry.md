# System Boundary (Frozen)

## System Kya Karega

- Physical AI & Humanoid Robotics ka structured textbook host karega
- Docusaurus-based frontend ke zariye content present karega
- Embedded RAG-based AI chatbot provide karega jo sirf book ke content se jawab dega
- Logged-in users ke background ke mutabiq content personalize karega
- Chapters ko Urdu mein translate karne ka option dega

## System Kya Nahi Karega

- Real humanoid ya physical robot ko control nahi karega
- ROS 2 nodes, launch files ya hardware drivers execute nahi karega
- Gazebo, Isaac Sim ya Unity simulations run nahi karega
- Live sensor data (camera, lidar, IMU) ingest nahi karega

## Boundary Rationale

Is project ka focus:
- AI-native education
- Spec-driven system design
- Agent-based intelligence

Is project ka focus nahi:
- Robotics hardware engineering
- Real-time control systems
- Production-grade robot deployment

Ye system boundary final aur frozen hai.
Iske baad koi feature is boundary ke bahar add nahi kiya ja sakta.
