# API Contracts: Module 3: The AI-Robot Brain (NVIDIA Isaac)

This directory contains API contracts and interface definitions for Module 3: The AI-Robot Brain (NVIDIA Isaac).

Since this module focuses on documentation for NVIDIA Isaac Sim, Isaac ROS, and Nav2 concepts, the contracts here represent the conceptual interfaces and data flows that students need to understand when working with these technologies.

## Documentation Interfaces

### Isaac Sim Integration Interface
- Input: Robot model, environment configuration, sensor specifications
- Output: Simulated sensor data, physics simulation results
- Purpose: Understanding how to configure and interact with Isaac Sim

### Isaac ROS Perception Pipeline Interface
- Input: Raw sensor data (cameras, LiDAR, IMU)
- Output: Processed perception results (object detection, SLAM, etc.)
- Purpose: Understanding perception pipeline configuration and data flow

### Nav2 Navigation Interface
- Input: Map data, robot pose, navigation goal
- Output: Path plan, navigation commands
- Purpose: Understanding navigation system configuration and operation

## Educational Contracts

These contracts define the expected learning outcomes and conceptual understanding that students should achieve:

### Chapter 1 Contract
- Student can explain Isaac Sim's role in Physical AI
- Student understands synthetic data generation concepts
- Student knows how Isaac Sim integrates with ROS 2

### Chapter 2 Contract
- Student can describe Isaac ROS capabilities
- Student understands hardware-accelerated VSLAM
- Student knows how to configure perception pipelines for humanoids

### Chapter 3 Contract
- Student can explain humanoid navigation challenges
- Student understands Nav2 architecture
- Student knows how to link perception to navigation