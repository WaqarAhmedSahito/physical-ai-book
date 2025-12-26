---
sidebar_label: 'ROS 2 Communication Primitives'
sidebar_position: 2
---

# Chapter 2: ROS 2 Communication Primitives

## Nodes, Topics, Services, and Actions

ROS 2 provides four primary communication patterns that enable different types of interactions between nodes:

### Nodes
Nodes are the fundamental building blocks of any ROS 2 application. Each node:
- Contains a specific piece of functionality
- Can publish messages to topics
- Can subscribe to messages from topics
- Can provide or use services
- Can send or execute actions

### Topics
Topics enable asynchronous, decoupled communication between nodes:
- Publisher-subscriber pattern
- Multiple publishers can send to one topic
- Multiple subscribers can receive from one topic
- Messages are delivered on a "best effort" or "reliable" basis
- Used for continuous data streams (sensor data, robot state)

### Services
Services enable synchronous request-response communication:
- Client-server pattern
- Request-response model
- Blocking calls until response is received
- Used for discrete operations (navigation goals, parameter updates)

### Actions
Actions provide asynchronous request-response with feedback:
- Extended service pattern with feedback during execution
- Goal, feedback, and result messages
- Ability to cancel ongoing operations
- Used for long-running operations (navigation, manipulation)

## Message passing and real-time considerations

### Quality of Service (QoS) Settings
ROS 2 provides QoS policies to handle real-time requirements:

- **Reliability**: Reliable vs. best effort delivery
- **Durability**: Volatile vs. transient local durability
- **History**: Keep last N messages vs. keep all messages
- **Deadline**: Maximum time between consecutive messages
- **Liveliness**: How to detect if a publisher is alive

### Real-time Performance
- DDS middleware handles message routing efficiently
- Configurable threading models
- Memory allocation strategies for real-time systems
- Support for real-time operating systems

## Writing Python-based ROS 2 nodes using rclpy

The `rclpy` library provides the Python client library for ROS 2:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Bridging AI agents (Python logic) with ROS controllers

### Integration Patterns
- **Direct Integration**: AI agents run as ROS 2 nodes
- **Bridge Nodes**: Specialized nodes translate between AI framework and ROS 2
- **Service-based**: AI agents call ROS 2 services to control robots
- **Topic-based**: AI agents publish to ROS 2 topics for robot control

### Common Bridge Scenarios
- Machine learning models providing perception results
- Planning algorithms generating robot trajectories
- Reinforcement learning agents controlling robot behavior
- Natural language processing for command interpretation

## Conceptual diagrams for communication flows

### Basic Publisher-Subscriber Flow:
```
[Sensor Node]     [Processing Node]     [Actuator Node]
      |                   |                   |
   publishes    ------> subscribes       publishes
      |                   |                   |
   sensor data      processes data      control commands
      |                   |                   |
   (topic: /sensors)  (topic: /processed) (topic: /cmd_vel)
```

### Service Request-Response:
```
[Requesting Node]              [Providing Node]
        |                            |
    sends request     -------->    receives request
        |                            |
    (service: /navigate)          processes request
        |                            |
    waits for response    <-------- provides response
        |                            |
    receives result              returns result
```

### Action with Feedback:
```
[Action Client]              [Action Server]
        |                          |
    sends goal        -------->   receives goal
        |                          |
    waits for result            starts execution
        |                          |
    receives feedback   <-------- sends feedback
        |                          |
    receives result     <-------- completes execution
        |                          |
    (action: /move_base)       (executes navigation)
```

## Tags
- communication
- nodes
- topics
- services
- actions