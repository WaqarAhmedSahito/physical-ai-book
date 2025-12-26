# API Contracts: Module 4: Vision-Language-Action (VLA)

This directory contains API contracts and interface definitions for Module 4: Vision-Language-Action (VLA).

Since this module focuses on documentation for VLA systems connecting perception, language, and action using LLMs and ROS 2, the contracts here represent the conceptual interfaces and data flows that engineers need to understand when working with these technologies.

## Documentation Interfaces

### Voice-to-Action Interface
- Input: Natural language voice commands
- Output: Structured robot intents
- Purpose: Understanding how voice input connects to robotic action systems

### LLM Planning Interface
- Input: High-level natural language commands
- Output: Sequenced robot action plans
- Purpose: Understanding how LLMs decompose tasks and generate executable actions

### ROS 2 Integration Interface
- Input: Structured action plans from LLM
- Output: ROS 2 messages and service calls
- Purpose: Understanding how VLA systems connect to robotic platforms

### Safety Constraint Interface
- Input: Planned robot actions
- Output: Validation results and safety boundaries
- Purpose: Understanding safety validation for autonomous systems

## Educational Contracts

These contracts define the expected learning outcomes and conceptual understanding that engineers should achieve:

### Chapter 1 Contract
- Engineer can explain the role of natural language in Physical AI
- Engineer understands OpenAI Whisper integration for voice commands
- Engineer knows speech-to-intent pipeline concepts
- Engineer understands ROS 2 integration for voice input

### Chapter 2 Contract
- Engineer can describe how LLMs translate natural language to robot actions
- Engineer understands task decomposition and sequencing techniques
- Engineer knows how to implement LLM-driven planners for ROS 2
- Engineer understands safety and execution constraints

### Chapter 3 Contract
- Engineer can design end-to-end VLA system architectures
- Engineer understands the complete pipeline from voice to action
- Engineer knows how to integrate vision, language, and control systems
- Engineer can evaluate autonomous humanoid systems