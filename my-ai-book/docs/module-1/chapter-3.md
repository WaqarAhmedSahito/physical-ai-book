---
sidebar_label: 'Humanoid Robot Description with URDF'
sidebar_position: 3
---

# Chapter 3: Humanoid Robot Description with URDF

## Purpose of URDF in humanoid robotics

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. In humanoid robotics, URDF serves several critical purposes:

- **Kinematic Description**: Defines the physical structure of the robot including links and joints
- **Dynamic Properties**: Specifies mass, inertia, and other dynamic properties for simulation
- **Visual Representation**: Provides visual elements for displaying the robot in tools like RViz
- **Collision Geometry**: Defines collision shapes for physics simulation
- **Transmission Information**: Describes how actuators connect to joints

URDF is essential for humanoid robots because it allows for:
- Consistent representation across simulation and real hardware
- Automatic generation of kinematic models
- Integration with ROS tools for visualization, simulation, and control

## Links, joints, and kinematic chains

### Links
Links represent rigid bodies in the robot structure:
- Each link has physical properties (mass, inertia, visual/collision geometry)
- Links are connected by joints to form the robot structure
- Examples in humanoid robots: head, torso, upper arm, lower arm, hand, thigh, shank, foot

### Joints
Joints connect links and define their relative motion:
- **Fixed joints**: No relative motion between links (welded connection)
- **Revolute joints**: Single degree of freedom rotation (like a hinge)
- **Continuous joints**: Revolute joints that can rotate continuously
- **Prismatic joints**: Single degree of freedom linear motion
- **Floating joints**: 6 degrees of freedom (rarely used)

### Kinematic Chains
Kinematic chains define the structure from base to end-effectors:
- **Forward kinematics**: Calculate end-effector position from joint angles
- **Inverse kinematics**: Calculate joint angles to achieve desired end-effector position
- **Tree structures**: Handle robots with multiple end-effectors (arms, legs)

## Modeling humanoid structure (arms, legs, torso, head)

### Typical Humanoid Structure
```
          head
            |
          torso
         /     \
    left arm   right arm
         \     /
          waist
         /     \
    left leg   right leg
```

### Arm Structure (example for one arm)
```
torso
  |
shoulder_pan_joint (revolute)
  |
upper_arm_link
  |
shoulder_lift_joint (revolute)
  |
lower_arm_link
  |
elbow_joint (revolute)
  |
forearm_link
  |
wrist_joint (revolute)
  |
hand_link
```

### Leg Structure (example for one leg)
```
torso
  |
hip_yaw_joint (revolute)
  |
thigh_link
  |
hip_pitch_joint (revolute)
  |
shank_link
  |
ankle_joint (revolute)
  |
foot_link
```

## How URDF connects ROS 2 with simulators (Gazebo / Isaac)

### URDF in Simulation
- **Gazebo**: Reads URDF files to create physics models for simulation
- **Isaac Sim**: Uses URDF as a starting point for more detailed simulation models
- **RViz**: Visualizes URDF models for debugging and monitoring

### Integration Process
1. URDF file is loaded by the simulator
2. Physics properties are extracted for simulation
3. Visual models are created for rendering
4. Joint controllers are instantiated
5. Sensor models are configured based on URDF specifications

### ROS 2 Integration
- Robot State Publisher node uses URDF to publish TF transforms
- Joint State Publisher provides joint position information
- Controllers use URDF to understand robot kinematics
- MoveIt! planning uses URDF for collision checking and inverse kinematics

## Common URDF mistakes and best practices

### Common Mistakes
1. **Incorrect Mass Properties**: Setting mass to 0 or unrealistic values
2. **Missing Inertia Tensors**: Not defining proper inertia properties
3. **Wrong Joint Limits**: Setting joint limits outside physical capabilities
4. **Collision vs Visual Mismatch**: Using different geometries for collision and visual
5. **Incorrect Origins**: Wrong origin definitions causing misalignment
6. **Overly Complex Geometry**: Using detailed meshes for collision detection

### Best Practices
1. **Start Simple**: Begin with basic geometric shapes, add complexity gradually
2. **Use xacro**: Xacro (XML Macros) helps create parameterized, reusable URDFs
3. **Validate Regularly**: Use `check_urdf` tool to validate URDF files
4. **Realistic Physics**: Use actual robot mass and inertia properties
5. **Appropriate Meshes**: Use simple shapes for collision, detailed meshes for visual
6. **Consistent Units**: Use consistent units throughout (SI units recommended)
7. **Documentation**: Comment complex URDF sections for maintainability

### Xacro Example
```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="simple_humanoid">
  <!-- Define properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.2 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Include other components using xacro:include -->
  <xacro:include filename="$(find my_robot_description)/urdf/arm.urdf.xacro" />
  <xacro:include filename="$(find my_robot_description)/urdf/leg.urdf.xacro" />
</robot>
```

## Tags
- urdf
- robotics
- modeling
- simulation