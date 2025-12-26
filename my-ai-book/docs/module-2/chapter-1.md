---
title: Physics Simulation with Gazebo
---

# Physics Simulation with Gazebo

## The Role of Digital Twins in Physical AI

Digital twins are virtual representations of physical systems that enable simulation, testing, and development without requiring physical hardware. In the context of Physical AI and robotics, digital twins serve as critical tools for:

1. **Development**: Test algorithms and behaviors without risk to expensive physical hardware
2. **Training**: Develop and refine AI models in a controlled, repeatable environment
3. **Validation**: Verify robot behaviors before deployment to real hardware
4. **Prototyping**: Experiment with new designs and capabilities without manufacturing costs

For humanoid robots, digital twins are particularly valuable because they allow developers to:
- Test complex locomotion algorithms safely
- Validate control systems without risk of robot falls or damage
- Experiment with different environmental conditions
- Train perception and decision-making systems with labeled data

## Physics Simulation Fundamentals

Physics simulation in robotics involves modeling the fundamental physical properties and interactions that govern how robots move and interact with their environment. These include:

- **Gravity**: The constant downward force that affects all objects
- **Collisions**: How objects interact when they come into contact
- **Dynamics**: The relationship between forces acting on a body and its motion
- **Friction**: The resistance that occurs when surfaces move against each other

Gazebo provides a robust physics engine that accurately simulates these properties, allowing developers to create realistic virtual environments for testing humanoid robots.

## Why Gazebo for Physics Simulation

Gazebo is specifically designed for robotics simulation and offers several advantages:

- **Accurate Physics**: Built-in physics engines (ODE, Bullet, SimBody) that accurately model real-world physics
- **Robot Integration**: Native support for robot models via URDF/SDF formats
- **Sensor Simulation**: Realistic simulation of various robot sensors
- **ROS Integration**: Seamless integration with ROS and ROS 2 for communication
- **Extensibility**: Plugin architecture for custom sensors, controllers, and environments

## Common Applications in Humanoid Robotics

Physics simulation with Gazebo is commonly used for:
- Testing walking and locomotion algorithms
- Validating balance and fall recovery systems
- Simulating interaction with objects and environments
- Training control policies before real-world deployment

## Foundational Concepts of Physics Simulation Environments

Physics simulation environments like Gazebo are built on several foundational concepts that enable realistic robot simulation:

### Simulation Loop
The simulation runs in discrete time steps, typically at a fixed rate (e.g., 1000 Hz). During each step:
1. Physics calculations are performed to determine forces, collisions, and motion
2. Robot states are updated based on the physics calculations
3. Sensor data is generated based on the updated states
4. Control commands are processed and applied to the simulated robot

### Coordinate Systems
Robots and environments are defined using coordinate systems:
- **World Frame**: The global reference frame for the entire simulation
- **Robot Base Frame**: The reference frame attached to the robot's base
- **Link Frames**: Individual frames attached to each robot link
- **Sensor Frames**: Frames defining the position and orientation of simulated sensors

### Rigid Body Dynamics
Physical objects in simulation are modeled as rigid bodies with properties such as:
- Mass and center of mass
- Inertia tensor
- Collision geometry
- Surface properties (friction coefficients, restitution)

### Integration Methods
Physics engines use numerical integration methods to solve equations of motion:
- Euler integration (simple but less accurate)
- Runge-Kutta methods (more accurate but computationally expensive)
- Semi-implicit methods (balance between accuracy and performance)

## Benefits of Simulation Over Physical Robot Testing

Using digital twins and simulation environments offers significant advantages over physical robot testing:

### Safety and Risk Mitigation
- **No Hardware Damage**: Testing aggressive behaviors or failure cases doesn't risk damaging expensive hardware
- **Controlled Environment**: Test scenarios can be precisely controlled and repeated
- **Failure Analysis**: Study failure modes safely without physical consequences

### Cost and Time Efficiency
- **Reduced Hardware Costs**: No need for multiple physical prototypes
- **Faster Iteration**: Modify robot parameters or environments instantly
- **Parallel Testing**: Run multiple experiments simultaneously in virtual environments

### Enhanced Learning and Development
- **Ground Truth Data**: Access to perfect state information for training and validation
- **Environmental Control**: Test in various conditions (weather, lighting, terrain) without physical setup
- **Repeatability**: Identical conditions for comparing different algorithms
- **Scalability**: Test on multiple virtual robots simultaneously

### Development Acceleration
- **Early Validation**: Test algorithms before hardware is available
- **Algorithm Refinement**: Optimize performance in simulation before real-world deployment
- **Integration Testing**: Validate complex multi-system interactions safely

## How Digital Twins Enable Robot Development and Testing

Digital twins serve as a bridge between theoretical robot design and practical implementation, enabling a comprehensive development workflow:

### Design and Prototyping Phase
Digital twins allow engineers to:
- Test kinematic and dynamic properties of robot designs
- Validate mechanical constraints and joint limits
- Assess the feasibility of planned motions and behaviors
- Identify potential design flaws before manufacturing

### Control System Development
In the control system development phase, digital twins provide:
- A safe environment to test control algorithms
- Access to ground truth state information for algorithm tuning
- The ability to test extreme conditions without hardware risk
- Validation of sensor fusion and state estimation algorithms

### Perception System Training
For perception systems, digital twins offer:
- Labeled training data generation for machine learning
- Controlled testing of perception algorithms under various conditions
- Simulation of sensor noise and imperfections
- Validation of computer vision and object detection systems

### Behavior and Planning Validation
Digital twins enable validation of:
- Path planning and navigation algorithms
- Task planning and execution sequences
- Human-robot interaction scenarios
- Multi-robot coordination strategies

### Deployment Preparation
Before deploying to physical hardware, digital twins allow:
- Comprehensive testing of complete robot behaviors
- Identification of edge cases and failure modes
- Performance benchmarking and optimization
- Safety validation under various operating conditions

## Examples and Use Cases for Digital Twins in Physical AI

Digital twins have been successfully applied in various Physical AI applications:

### Humanoid Robot Development
- **Boston Dynamics**: Uses simulation extensively for developing dynamic locomotion behaviors
- **Agility Robotics**: Employs digital twins to test and refine Cassie's walking algorithms
- **ANYbotics**: Utilizes simulation for developing legged robots for challenging terrains

### Industrial Robotics
- **ABB and KUKA**: Use digital twins for programming and validating industrial robot motions
- **Amazon Robotics**: Employs simulation for warehouse automation system design and testing
- **Fanuc**: Implements digital twins for predictive maintenance and performance optimization

### Autonomous Systems
- **Tesla**: Uses simulation environments for training and validating autonomous driving systems
- **Waymo**: Employs extensive simulation for testing self-driving car behaviors
- **Agricultural Robotics**: Companies like Blue River Technology use simulation for developing crop management robots

### Research Applications
- **OpenAI Robotics**: Uses simulated environments to train dexterous manipulation skills
- **ETH Zurich**: Employs digital twins for testing complex multi-robot coordination
- **MIT CSAIL**: Utilizes simulation for developing novel robot morphologies and control strategies

### Educational Use Cases
- **Robotics Courses**: Universities use simulation environments to teach robotics concepts safely
- **Competitions**: RoboCup and other competitions often include simulated leagues
- **Skill Transfer Research**: Studies on how to effectively transfer skills from simulation to reality

# Simulating Physical Properties in Gazebo

## Gravity Simulation

Gazebo simulates gravity by applying a constant downward acceleration to all objects in the simulation world. The default gravity setting is typically 9.8 m/s² (Earth's gravity), but this can be customized:

- **Global Gravity**: Set in the world file to affect the entire simulation environment
- **Body-Specific Gravity**: Can be overridden for individual objects if needed
- **Direction**: Usually points downward in the negative Z direction (0, 0, -9.8)

Gravity affects:
- Robot locomotion and balance
- Object falling and settling
- Cable and rope dynamics
- Fluid simulation (if using fluid plugins)

## Collision Detection

Collision detection in Gazebo involves several key concepts:

### Collision Shapes
- **Primitive Shapes**: Boxes, spheres, and cylinders for simple objects
- **Mesh Collisions**: Complex shapes using triangle meshes
- **Compound Shapes**: Combinations of primitive shapes for complex objects

### Contact Detection
- **Contact Points**: Points where objects touch or intersect
- **Contact Forces**: Forces generated at contact points to prevent interpenetration
- **Friction Models**: Static and dynamic friction between surfaces
- **Bounce Properties**: How objects react when they hit each other

### Collision Algorithms
- **Broad Phase**: Fast elimination of object pairs that cannot collide
- **Narrow Phase**: Precise collision detection between potentially colliding objects
- **Continuous Collision Detection**: Prevents objects from passing through each other at high speeds

## Dynamics Simulation

Dynamics simulation encompasses how forces affect motion:

### Newtonian Mechanics
- **Linear Motion**: F = ma (Force equals mass times acceleration)
- **Rotational Motion**: τ = Iα (Torque equals moment of inertia times angular acceleration)
- **Joint Constraints**: Limiting degrees of freedom in robot joints

### Force Integration
- **Forward Euler**: Simple but can be unstable with large time steps
- **Runge-Kutta**: More accurate but computationally expensive
- **Semi-Implicit**: Good balance of accuracy and stability

### Joint Dynamics
- **Revolute Joints**: Single-axis rotation (like hinges)
- **Prismatic Joints**: Linear translation along one axis
- **Fixed Joints**: No relative motion between connected links
- **Floating Joints**: Six degrees of freedom between links

## Practical Considerations

### Simulation Accuracy vs Performance
- **Time Step**: Smaller steps increase accuracy but decrease performance
- **Iterations**: More solver iterations improve contact handling
- **Tolerance**: Error tolerance affects solution quality

### Tuning Parameters
- **ERP (Error Reduction Parameter)**: Controls how quickly constraint errors are corrected
- **CFM (Constraint Force Mixing)**: Adds compliance to constraints to prevent numerical instability
- **Friction Coefficients**: Static and dynamic friction values for realistic contact behavior

## Gazebo Physics Engine Fundamentals

Gazebo supports multiple physics engines, each with different characteristics and strengths:

### Open Dynamics Engine (ODE)
- **Strengths**: Fast, stable for most robotics applications
- **Use Cases**: General-purpose robotics simulation, real-time applications
- **Characteristics**: Good for rigid body simulation with contacts
- **Limitations**: Can be unstable with complex contact scenarios

### Bullet Physics
- **Strengths**: More robust contact handling, better for complex interactions
- **Use Cases**: Applications requiring accurate collision detection
- **Characteristics**: More computationally intensive but more stable
- **Limitations**: Slower than ODE for simple scenarios

### SimBody
- **Strengths**: High-fidelity simulation for complex articulated systems
- **Use Cases**: Applications requiring high accuracy in joint constraints
- **Characteristics**: Excellent for biomechanical simulation
- **Limitations**: More complex to configure and computationally expensive

### Physics Engine Configuration

The physics engine is configured in the world file:

```xml
<world name="default">
  <physics type="ode">
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1.0</real_time_factor>
    <real_time_update_rate>1000.0</real_time_update_rate>
    <gravity>0 0 -9.8</gravity>
  </physics>
</world>
```

### Key Physics Parameters

**Time Step**: The duration of each simulation step (typically 0.001 seconds)
- Smaller steps increase accuracy but require more computation
- Must be small enough to capture the fastest dynamics in the system

**Real-time Factor**: Ratio of simulation time to real time
- 1.0 means simulation runs at real-time speed
- Values > 1.0 mean simulation runs faster than real time
- Values < 1.0 mean simulation runs slower than real time

**Update Rate**: How frequently the physics engine updates
- Related to time step by: update_rate = 1 / max_step_size
- Higher rates provide more accurate simulation but require more processing power

### Solver Parameters

**Iterations**: Number of iterations for solving constraints
- More iterations provide more accurate contact handling
- More iterations require more computation time
- Typical values range from 50 to 200

**SOR (Successive Over-Relaxation)**: Parameter for iterative solvers
- Controls the convergence rate of the solver
- Values around 1.0-1.3 are typically effective

# Integrating Gazebo with ROS 2

## Overview of Gazebo-ROS Integration

Gazebo integrates with ROS 2 through the `gazebo_ros_pkgs` package, which provides plugins and tools that enable communication between the simulation environment and ROS 2 nodes. This integration allows:

- Publishing simulated sensor data to ROS 2 topics
- Subscribing to ROS 2 topics to control simulated robots
- Using ROS 2 services and actions for simulation control
- Managing robot models and simulation states through ROS 2

## Gazebo ROS Plugins

The integration is primarily achieved through plugins that connect Gazebo simulation elements to ROS 2:

### Sensor Plugins
- **Camera Plugins**: Publish images to `sensor_msgs/Image` topics
- **LIDAR Plugins**: Publish laser scan data to `sensor_msgs/LaserScan` topics
- **IMU Plugins**: Publish inertial measurement data to `sensor_msgs/Imu` topics
- **Force/Torque Plugins**: Publish force and torque measurements

### Actuator Plugins
- **Joint Control Plugins**: Subscribe to joint command topics to control robot joints
- **Effort Control Plugins**: Apply forces/torques to joints
- **Velocity Control Plugins**: Control joint velocities
- **Position Control Plugins**: Control joint positions

### Communication Plugins
- **ROS Bridge**: General-purpose bridge for custom message types
- **Model States Publisher**: Publishes model poses and twists
- **Joint States Publisher**: Publishes joint positions, velocities, and efforts

## URDF Integration

Robot models are typically defined in URDF (Unified Robot Description Format) with additional Gazebo-specific tags:

```xml
<robot name="my_robot">
  <!-- Standard URDF content -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="1 1 1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="1 1 1"/>
      </geometry>
    </collision>
  </link>

  <!-- Gazebo-specific content -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <!-- Sensor plugin example -->
  <gazebo reference="lidar_link">
    <sensor type="ray" name="lidar_sensor">
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.10</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>/lidar</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

## Launching Gazebo with ROS 2

Gazebo simulations are typically launched using ROS 2 launch files:

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        # Launch Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('gazebo_ros'),
                    'launch',
                    'gazebo.launch.py'
                ])
            ]),
            launch_arguments={
                'world': PathJoinSubstitution([
                    FindPackageShare('my_robot_gazebo'),
                    'worlds',
                    'my_world.world'
                ])
            }.items()
        ),

        # Spawn robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'my_robot'
            ],
            output='screen'
        )
    ])
```

## Common Integration Patterns

### Robot State Publishing
- Use `robot_state_publisher` to broadcast TF transforms
- Gazebo publishes joint states, which are consumed by the state publisher
- TF tree allows for coordinate transformations between robot parts

### Control Systems
- Implement controllers using `ros2_control` framework
- Use joint trajectory controllers for position/velocity/effort control
- Implement custom controllers for specific robot behaviors

### Sensor Data Processing
- Subscribe to sensor topics in ROS 2 nodes
- Process simulated sensor data the same way as real sensor data
- Use the same algorithms for both simulation and real robots

# Common Gazebo Simulation Pitfalls and How to Avoid Them

## Physics-Related Pitfalls

### Unstable Simulations
**Problem**: Robot joints oscillate wildly or the simulation becomes unstable.
**Solutions**:
- Reduce the simulation time step (e.g., from 0.01 to 0.001 seconds)
- Increase the number of physics solver iterations
- Adjust ERP and CFM parameters for joints
- Ensure proper mass and inertia properties for all links

### Penetration Issues
**Problem**: Objects pass through each other or fail to make proper contact.
**Solutions**:
- Increase the number of physics iterations
- Use more accurate collision meshes
- Enable continuous collision detection for fast-moving objects
- Adjust surface contact parameters (mu, kp, kd)

### Gravity and Balance Problems
**Problem**: Robots fall over unexpectedly or behave unrealistically.
**Solutions**:
- Verify center of mass is correctly calculated
- Check that inertia tensors are properly defined
- Ensure joint limits and effort/torque constraints are realistic
- Use appropriate friction coefficients for contact surfaces

## Performance Pitfalls

### Slow Simulation Speed
**Problem**: Simulation runs much slower than real-time.
**Solutions**:
- Simplify collision meshes (use boxes/cylinders instead of complex meshes)
- Reduce the number of contacts in the scene
- Use simpler physics engine settings for early development
- Limit the number of active sensors or reduce their update rates

### High CPU Usage
**Problem**: Simulation consumes excessive CPU resources.
**Solutions**:
- Reduce the physics update rate if high fidelity isn't required
- Disable unnecessary plugins or sensors
- Use less computationally expensive physics engine settings
- Close other applications to free up system resources

## Model-Related Pitfalls

### Incorrect URDF Definitions
**Problem**: Robot model behaves unexpectedly or doesn't move properly.
**Solutions**:
- Verify joint limits, effort, and velocity limits are realistic
- Ensure visual and collision meshes are properly aligned
- Check that all required transmissions are defined
- Validate that joint axes are correctly oriented

### Mass and Inertia Issues
**Problem**: Robot doesn't respond properly to forces or control commands.
**Solutions**:
- Use CAD software to calculate accurate mass and inertia properties
- Ensure the total robot mass is realistic
- Verify inertia tensors are positive definite
- Check that center of mass is within the physical bounds of the robot

## Sensor Simulation Pitfalls

### Unrealistic Sensor Data
**Problem**: Sensor data doesn't match expectations or real-world behavior.
**Solutions**:
- Verify sensor noise parameters match real sensor characteristics
- Check sensor mounting positions and orientations
- Ensure sensor ranges and fields of view are appropriate
- Validate that sensor frame IDs match TF tree expectations

### Timing and Synchronization Issues
**Problem**: Sensor data arrives at unexpected times or is out of sync.
**Solutions**:
- Understand the relationship between physics steps and sensor updates
- Configure appropriate update rates for different sensor types
- Use ROS 2 message filters for time synchronization when needed
- Account for simulation time vs. real time in your nodes

## Integration Pitfalls

### ROS Communication Problems
**Problem**: ROS nodes can't communicate properly with Gazebo.
**Solutions**:
- Verify ROS master URI and network configuration
- Check that topic names match between publishers and subscribers
- Ensure correct message types are being used
- Use `ros2 topic list` and `ros2 topic echo` to debug communication

### TF Tree Issues
**Problem**: Coordinate transforms are incorrect or missing.
**Solutions**:
- Verify that robot_state_publisher is running correctly
- Check that all required frames are published
- Ensure joint names match between URDF and controller configuration
- Use `ros2 run tf2_tools view_frames` to visualize the TF tree

## Best Practices to Avoid Pitfalls

### Start Simple
- Begin with basic shapes and simple physics
- Gradually add complexity once the basic setup works
- Test individual components before integrating them

### Validate Regularly
- Use Gazebo's built-in visualization tools to verify physics behavior
- Monitor ROS topics to ensure data is flowing correctly
- Test control algorithms in simulation before real hardware deployment

### Document Configuration
- Keep track of working physics parameters
- Document any custom configurations or workarounds
- Maintain separate configurations for different use cases

# Practical Examples of Gazebo Physics Simulation for Humanoid Robots

## Simple Humanoid Model Setup

Let's examine a basic humanoid model with essential components:

```xml
<robot name="simple_humanoid">
  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.004" ixy="0" ixz="0" iyy="0.004" iyz="0" izz="0.004"/>
    </inertial>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.416" ixy="0" ixz="0" iyy="0.525" iyz="0" izz="0.225"/>
    </inertial>
  </link>

  <!-- Hip joint connecting head to torso -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.35" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
  </joint>

  <!-- Gazebo-specific configurations -->
  <gazebo reference="head">
    <material>Gazebo/Blue</material>
  </gazebo>
  <gazebo reference="torso">
    <material>Gazebo/Orange</material>
  </gazebo>
</robot>
```

## Balance and Stability Simulation

### Center of Mass Considerations
For humanoid robots, maintaining balance is critical:
- The center of mass should remain within the support polygon
- Lower centers of mass provide greater stability
- Dynamic balance requires continuous adjustment of body position

### Simulation Parameters for Balance
```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/humanoid</robotNamespace>
    <controlPeriod>0.001</controlPeriod>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
  </plugin>
</gazebo>
```

## Walking Gait Simulation

### Basic Walking Controller
A simple walking gait can be simulated by coordinating leg movements:

1. **Swing Phase**: One leg moves forward while the other supports
2. **Stance Phase**: Weight is transferred to the forward leg
3. **Double Support**: Brief period when both feet contact the ground

### Joint Trajectory Control
```python
# Example Python code for controlling humanoid walking
import rclpy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

def create_step_trajectory():
    trajectory = JointTrajectory()
    trajectory.joint_names = ["left_hip", "right_hip", "left_knee", "right_knee"]

    # Define key points in the walking motion
    point1 = JointTrajectoryPoint()
    point1.positions = [0.0, 0.0, 0.0, 0.0]  # Standing position
    point1.time_from_start = Duration(sec=1)

    point2 = JointTrajectoryPoint()
    point2.positions = [0.1, -0.1, 0.2, -0.2]  # Step forward
    point2.time_from_start = Duration(sec=2)

    trajectory.points = [point1, point2]
    return trajectory
```

## Manipulation and Grasping

### Hand and Arm Simulation
Humanoid robots often need to manipulate objects:

```xml
<!-- Example of a simple gripper -->
<link name="left_hand">
  <visual>
    <geometry>
      <box size="0.05 0.1 0.05"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.05 0.1 0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.2"/>
    <inertia ixx="0.00017" ixy="0" ixz="0" iyy="0.00008" iyz="0" izz="0.00017"/>
  </inertial>
</link>

<!-- Fixed joint to attach hand to arm -->
<joint name="left_wrist" type="fixed">
  <parent link="left_forearm"/>
  <child link="left_hand"/>
  <origin xyz="0 0 -0.05" rpy="0 0 0"/>
</joint>
```

## Environmental Interaction

### Ground Contact
Humanoid robots need to interact stably with the ground:
- Proper friction coefficients for realistic foot-ground interaction
- Appropriate compliance to handle uneven surfaces
- Sufficient collision geometry to prevent penetration

### Object Manipulation
When interacting with objects:
- Ensure adequate gripper force limits
- Model object properties (mass, friction, elasticity)
- Consider the dynamic effects of object manipulation on robot balance

## Performance Optimization Examples

### Simplified Collision Models
For better performance while maintaining accuracy:

```xml
<!-- Complex visual model -->
<link name="visual_body">
  <visual>
    <geometry>
      <mesh filename="humanoid_body.dae"/>
    </geometry>
  </visual>
</link>

<!-- Simple collision model -->
<link name="collision_body">
  <collision>
    <geometry>
      <box size="0.3 0.2 0.5"/>  <!-- Simple box approximation -->
    </geometry>
  </collision>
</link>
```

### Physics Parameter Tuning
Example of optimized physics parameters for humanoid simulation:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000.0</real_time_update_rate>
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.000001</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

These examples demonstrate how to set up and configure humanoid robots in Gazebo for realistic physics simulation, from basic models to complex behaviors like walking and manipulation.