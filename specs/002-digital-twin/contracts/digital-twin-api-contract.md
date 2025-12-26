# API Contract: Digital Twin Simulation Interface

**Module**: Module 2: The Digital Twin (Gazebo & Unity)
**Version**: 1.0
**Date**: 2025-12-17

## Overview

This document defines the API contract for digital twin simulation interfaces in the context of robotics education. It specifies how educational content, simulation environments, and ROS integration components interact to provide a comprehensive learning experience about digital twins for humanoid robots.

## API Endpoints

### 1. Simulation Environment Management

#### GET /api/simulation/environments
- **Purpose**: Retrieve available simulation environments (Gazebo, Unity)
- **Response**:
  ```json
  {
    "environments": [
      {
        "id": "gazebo",
        "name": "Gazebo Physics Simulation",
        "type": "physics",
        "description": "Physics-based simulation environment for dynamics and collisions",
        "version": "11.x",
        "supported_features": ["dynamics", "collisions", "sensors", "ROS_integration"]
      },
      {
        "id": "unity",
        "name": "Unity High-Fidelity Visualization",
        "type": "visualization",
        "description": "High-fidelity visualization environment for human-robot interaction",
        "version": "2021.3 LTS",
        "supported_features": ["graphics", "lighting", "materials", "interaction"]
      }
    ]
  }
  ```

#### POST /api/simulation/session
- **Purpose**: Initialize a new simulation session
- **Request**:
  ```json
  {
    "environment_id": "gazebo",
    "world_file": "default_humanoid.world",
    "robot_model": "humanoid_robot.urdf",
    "session_name": "physics_simulation_tutorial"
  }
  ```
- **Response**:
  ```json
  {
    "session_id": "sess_12345",
    "status": "initialized",
    "connection_info": {
      "ros_master_uri": "http://localhost:11311",
      "simulation_port": 11345,
      "gui_available": true
    }
  }
  ```

### 2. Robot Model Management

#### GET /api/robot/models
- **Purpose**: Retrieve available robot models for simulation
- **Response**:
  ```json
  {
    "models": [
      {
        "id": "simple_humanoid",
        "name": "Simple Humanoid Robot",
        "type": "humanoid",
        "description": "Basic humanoid robot model for learning",
        "sensors": ["imu", "lidar", "camera"],
        "joints": 12,
        "links": 13
      }
    ]
  }
  ```

#### POST /api/robot/spawn
- **Purpose**: Spawn a robot model in the simulation environment
- **Request**:
  ```json
  {
    "model_id": "simple_humanoid",
    "position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
    "namespace": "/robot1"
  }
  ```
- **Response**:
  ```json
  {
    "spawn_status": "success",
    "robot_id": "robot1_123",
    "ros_topics": {
      "joint_states": "/robot1/joint_states",
      "tf": "/robot1/tf",
      "imu": "/robot1/imu/data",
      "lidar": "/robot1/laser_scan"
    }
  }
  ```

### 3. Sensor Data Interface

#### GET /api/sensors/data/{robot_id}
- **Purpose**: Retrieve current sensor data from a simulated robot
- **Response**:
  ```json
  {
    "robot_id": "robot1_123",
    "timestamp": "2025-12-17T10:30:00Z",
    "sensors": {
      "imu": {
        "linear_acceleration": {"x": 0.1, "y": -0.2, "z": 9.8},
        "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.01},
        "orientation": {"x": 0.0, "y": 0.0, "z": 0.01, "w": 1.0}
      },
      "lidar": {
        "ranges": [2.5, 2.4, 2.6, ...], // Array of distance measurements
        "intensities": [100, 100, 95, ...], // Array of intensity values
        "angle_min": -3.14159,
        "angle_max": 3.14159,
        "angle_increment": 0.01745
      },
      "camera": {
        "image_data": "base64_encoded_image",
        "width": 640,
        "height": 480,
        "encoding": "rgb8"
      }
    }
  }
  ```

### 4. Simulation Control

#### POST /api/simulation/control
- **Purpose**: Control simulation execution (start, pause, reset)
- **Request**:
  ```json
  {
    "session_id": "sess_12345",
    "command": "start" // Options: start, pause, reset, stop
  }
  ```
- **Response**:
  ```json
  {
    "command": "start",
    "status": "executed",
    "simulation_time": 0.0
  }
  ```

### 5. Educational Content Interface

#### GET /api/education/content/{module_id}
- **Purpose**: Retrieve educational content for the digital twin module
- **Response**:
  ```json
  {
    "module_id": "module_2",
    "title": "The Digital Twin (Gazebo & Unity)",
    "chapters": [
      {
        "chapter_id": "chapter_1",
        "title": "Physics Simulation with Gazebo",
        "topics": [
          "Role of digital twins in Physical AI",
          "Simulating gravity, collisions, and dynamics",
          "Integrating Gazebo with ROS 2",
          "Common simulation pitfalls"
        ],
        "learning_objectives": [
          "Explain the role of digital twins in Physical AI",
          "Understand Gazebo physics simulation concepts",
          "Configure basic Gazebo environments"
        ]
      },
      {
        "chapter_id": "chapter_2",
        "title": "High-Fidelity Environments with Unity",
        "topics": [
          "Why Unity for human-robot interaction",
          "Visual realism vs physics accuracy",
          "ROS–Unity communication concepts",
          "Use cases for humanoid simulation"
        ],
        "learning_objectives": [
          "Understand when to use Unity vs Gazebo",
          "Explain visual realism vs physics accuracy trade-offs",
          "Describe ROS-Unity communication"
        ]
      },
      {
        "chapter_id": "chapter_3",
        "title": "Simulated Sensors for Humanoids",
        "topics": [
          "LiDAR, depth cameras, and IMUs",
          "Sensor noise and realism",
          "Sensor data flow into ROS 2",
          "Preparing for perception modules"
        ],
        "learning_objectives": [
          "Configure simulated sensors in digital twins",
          "Understand sensor noise and realism",
          "Trace sensor data flow into ROS 2"
        ]
      }
    ]
  }
  ```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

### Common Error Codes
- `INVALID_REQUEST`: Request parameters are invalid
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `SIMULATION_ERROR`: Error occurred in simulation environment
- `CONNECTION_ERROR`: Connection to simulation environment failed
- `PERMISSION_DENIED`: Insufficient permissions for the requested action

## Authentication

All API endpoints require authentication using API keys for educational use tracking and rate limiting:

- **Header**: `Authorization: Bearer {api_key}`
- **Rate Limit**: 100 requests per minute per API key

## Versioning

- **URL Versioning**: `/api/v1/` prefix for all endpoints
- **Backward Compatibility**: New versions will maintain backward compatibility for 12 months

## Data Formats

- **Request/Response**: JSON format for all API communications
- **Timestamps**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- **Coordinates**: Standard ROS coordinate frames (right-handed, X-forward, Y-left, Z-up)