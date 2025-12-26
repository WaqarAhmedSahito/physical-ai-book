# Data Model: Module 2: The Digital Twin (Gazebo & Unity)

**Feature**: Module 2: The Digital Twin (Gazebo & Unity)
**Date**: 2025-12-17
**Entity Extraction Source**: spec.md

## Entities

### 1. Digital Twin
- **Description**: A virtual representation of a physical robot system that enables simulation, testing, and development without requiring physical hardware
- **Attributes**:
  - id: unique identifier
  - name: human-readable name
  - type: robot type (humanoid, mobile, manipulator, etc.)
  - physical_properties: mass, dimensions, materials
  - kinematic_model: joint configurations, degrees of freedom
  - sensor_configurations: list of sensors attached to the twin
  - simulation_environment: associated simulation environment (Gazebo/Unity)
- **Relationships**:
  - Contains -> Simulated Robot Components
  - Connected to -> ROS Integration Layer
- **Validation Rules**:
  - Must have a unique identifier
  - Must be associated with a valid simulation environment
  - Must have at least one sensor configuration

### 2. Gazebo Simulation Environment
- **Description**: A physics-based simulation environment designed for robotics applications with realistic dynamics, collisions, and sensor simulation
- **Attributes**:
  - id: unique identifier
  - name: environment name
  - version: Gazebo version
  - physics_engine: underlying physics engine (ODE, Bullet, SimBody)
  - world_file: path to the world description file
  - gravity_settings: gravitational acceleration values
  - collision_models: collision mesh definitions
  - dynamics_parameters: friction, damping coefficients
- **Relationships**:
  - Contains -> Simulated Robots
  - Connected to -> ROS Integration Layer
- **Validation Rules**:
  - Must have a valid physics engine configured
  - World file must exist and be accessible
  - Gravity settings must be physically reasonable

### 3. Unity Simulation Environment
- **Description**: A high-fidelity visualization environment suitable for human-robot interaction scenarios with advanced graphics capabilities
- **Attributes**:
  - id: unique identifier
  - name: environment name
  - version: Unity version
  - graphics_quality: rendering quality settings
  - lighting_conditions: environmental lighting parameters
  - material_properties: surface appearance definitions
  - interaction_modes: supported human-robot interaction types
- **Relationships**:
  - Contains -> Simulated Robots
  - Connected to -> ROS Integration Layer
- **Validation Rules**:
  - Must have valid graphics quality settings
  - Interaction modes must be properly configured

### 4. Simulated Sensor
- **Description**: Virtual representations of physical sensors (LiDAR, depth cameras, IMUs) that generate realistic data for robot perception algorithms
- **Attributes**:
  - id: unique identifier
  - type: sensor type (LIDAR, Depth Camera, IMU, etc.)
  - name: human-readable name
  - position: 3D position relative to robot frame
  - orientation: 3D orientation relative to robot frame
  - noise_model: parameters for sensor noise simulation
  - field_of_view: sensor coverage area
  - range_limits: minimum and maximum sensing distances
  - update_rate: frequency of sensor data generation
  - data_format: format of sensor output
- **Relationships**:
  - Belongs to -> Digital Twin
  - Connected to -> ROS Integration Layer
- **Validation Rules**:
  - Type must be one of the supported sensor types
  - Position and orientation must be valid coordinates
  - Range limits must be physically reasonable

### 5. ROS Integration Layer
- **Description**: The communication layer that connects simulation environments with ROS 2 for seamless robot development and testing
- **Attributes**:
  - id: unique identifier
  - ros_distro: ROS distribution version (e.g., Humble Hawksbill)
  - node_name: name of the ROS node managing simulation
  - topics: list of ROS topics for data exchange
  - services: list of ROS services for control
  - message_types: supported ROS message types
  - connection_status: current connection state
- **Relationships**:
  - Connects -> Gazebo Simulation Environment
  - Connects -> Unity Simulation Environment
  - Connects -> Simulated Sensors
- **Validation Rules**:
  - Must be compatible with specified ROS distribution
  - Topics and services must follow ROS naming conventions
  - Connection must be established before data exchange

## Relationships

### Digital Twin Composition
- Digital Twin *contains* multiple Simulated Sensors
- Digital Twin *utilizes* one Simulation Environment (Gazebo or Unity)
- Digital Twin *integrates with* ROS Integration Layer

### Simulation Environment Capabilities
- Gazebo Simulation Environment *provides* Physics Simulation
- Unity Simulation Environment *provides* High-Fidelity Visualization
- Both *connect to* ROS Integration Layer

## State Transitions

### Digital Twin States
- Design: Twin is being configured with robot properties
- Simulation Ready: Twin is configured and ready for simulation
- Active Simulation: Twin is actively running in simulation environment
- Paused: Simulation is temporarily stopped
- Stopped: Simulation has ended

### Simulation Environment States
- Initialized: Environment is loaded but inactive
- Running: Environment is actively simulating
- Paused: Environment simulation is paused
- Error: Environment encountered an error condition

### ROS Integration States
- Disconnected: No connection to ROS network
- Connecting: Attempting to establish connection
- Connected: Active connection to ROS network
- Ready: Connection established and ready for data exchange
- Error: Connection error occurred

## Constraints

1. **Simulation Environment Exclusivity**: A single Digital Twin instance must use either Gazebo OR Unity, not both simultaneously
2. **ROS Compatibility**: All simulation environments must be compatible with the same ROS 2 distribution
3. **Sensor Configuration Limits**: Sensor configurations must not exceed computational resources available for real-time simulation
4. **Data Consistency**: Sensor data published to ROS must maintain temporal consistency across all simulated sensors
5. **Physical Plausibility**: All simulated physics must adhere to realistic physical constraints and laws