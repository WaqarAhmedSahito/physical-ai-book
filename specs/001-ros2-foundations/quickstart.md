# Quickstart Guide: Module 1: The Robotic Nervous System (ROS 2)

## Overview
This guide provides a quick setup and implementation path for Module 1 of the AI-Native Book with Embedded RAG Chatbot. This module covers ROS 2 as a robotic nervous system for AI students and software engineers.

## Prerequisites
- Node.js (version 18.x or higher)
- npm or yarn package manager
- Git for version control
- Basic knowledge of Markdown and JavaScript (helpful but not required)

## Setup Steps

### 1. Initialize Docusaurus Project
```bash
# Create a new Docusaurus project
npx create-docusaurus@latest my-ai-book classic

# Navigate to the project directory
cd my-ai-book
```

### 2. Install Additional Dependencies (if needed)
```bash
# Install any additional dependencies for enhanced functionality
npm install
```

### 3. Create Module 1 Directory Structure
```bash
# Create the module directory
mkdir -p docs/module-1

# Create the three chapter files
touch docs/module-1/chapter-1.md
touch docs/module-1/chapter-2.md
touch docs/module-1/chapter-3.md
```

### 4. Configure Sidebar Navigation
Update `sidebars.js` to include the new module and chapters:

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/chapter-1',
        'module-1/chapter-2',
        'module-1/chapter-3'
      ],
    },
    // ... other modules
  ],
};
```

### 5. Create Chapter Content

#### Chapter 1: Introduction to ROS 2 as a Robotic Nervous System
Create content covering:
- What ROS 2 is and why it is critical for Physical AI
- ROS 2 architecture overview (DDS, nodes, executors)
- Comparison with ROS 1 (real-time, reliability, scalability)
- How ROS 2 maps to biological nervous systems (sensors, actuators, signals)

#### Chapter 2: ROS 2 Communication Primitives
Create content covering:
- Nodes, Topics, Services, and Actions
- Message passing and real-time considerations
- Writing Python-based ROS 2 nodes using rclpy
- Bridging AI agents (Python logic) with ROS controllers
- Example communication flows (no full code, conceptual diagrams only)

#### Chapter 3: Humanoid Robot Description with URDF
Create content covering:
- Purpose of URDF in humanoid robotics
- Links, joints, and kinematic chains
- Modeling humanoid structure (arms, legs, torso, head)
- How URDF connects ROS 2 with simulators (Gazebo / Isaac)
- Common URDF mistakes and best practices

### 6. Configure for GitHub Pages
Update `docusaurus.config.js` with GitHub Pages settings:

```javascript
// docusaurus.config.js
module.exports = {
  // ... other config
  deploymentBranch: 'gh-pages',
  trailingSlash: undefined,
  // ... rest of config
};
```

### 7. Test the Setup
```bash
# Start the development server
npm run start

# Build the static site
npm run build

# Serve the built site locally for testing
npm run serve
```

### 8. Deploy to GitHub Pages
```bash
# Deploy to GitHub Pages
GIT_USER=<Your GitHub username> USE_SSH=true npm run deploy
```

## Next Steps
1. Review and refine the content based on the functional requirements
2. Add diagrams-as-text explanations where helpful
3. Ensure all content meets the success criteria defined in the specification
4. Prepare for integration with the RAG chatbot system (in future modules)