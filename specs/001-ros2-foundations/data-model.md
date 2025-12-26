# Data Model: Module 1: The Robotic Nervous System (ROS 2)

## Overview
This document describes the conceptual data model for Module 1 of the AI-Native Book. Since this is a documentation project, the "data model" refers to the content structure, metadata, and relationships between different pieces of information.

## Content Entities

### 1. Chapter
- **Name**: String (required)
- **ID**: String (unique identifier, auto-generated from name)
- **Title**: String (display title)
- **Content**: Markdown text (main content body)
- **Metadata**: Object containing:
  - `authors`: Array of strings
  - `lastUpdated`: Date
  - `version`: String
  - `tags`: Array of strings (e.g., ["ros2", "architecture", "communication"])
- **Navigation**: Object containing:
  - `previous`: Chapter ID or null
  - `next`: Chapter ID or null
  - `parent`: Module ID

### 2. Module
- **ID**: String (unique identifier, e.g., "module-1")
- **Title**: String (e.g., "The Robotic Nervous System (ROS 2)")
- **Description**: String (brief overview)
- **Chapters**: Array of Chapter references
- **LearningObjectives**: Array of strings (what users will learn)
- **Prerequisites**: Array of strings (what users should know beforehand)

### 3. Concept
- **ID**: String (unique identifier)
- **Name**: String (e.g., "DDS", "URDF", "Nodes")
- **Definition**: String (clear definition)
- **RelatedConcepts**: Array of Concept IDs
- **Examples**: Array of Example objects
- **UseCases**: Array of strings (practical applications)

### 4. Example
- **ID**: String (unique identifier)
- **Title**: String (brief description)
- **Code**: String (code snippet in appropriate language)
- **Explanation**: String (what the example demonstrates)
- **RelatedConcepts**: Array of Concept IDs

### 5. Diagram
- **ID**: String (unique identifier)
- **Title**: String (description)
- **Type**: String (e.g., "architecture", "flow", "structure")
- **Description**: String (text-based representation of the diagram)
- **RelatedConcepts**: Array of Concept IDs

## Relationships

### Module-Chapter Relationship
- One Module contains many Chapters
- Each Chapter belongs to exactly one Module

### Chapter-Concept Relationship
- One Chapter may introduce/cover many Concepts
- One Concept may be covered in multiple Chapters

### Concept-Example Relationship
- One Concept may have many Examples
- One Example typically demonstrates one primary Concept (but may relate to others)

### Concept-Diagram Relationship
- One Concept may have many Diagrams
- One Diagram may illustrate multiple Concepts

## Validation Rules

1. **Chapter Validation**:
   - Each chapter must have a unique title within its module
   - Each chapter must have content of at least 200 words
   - Each chapter must have properly formatted metadata

2. **Module Validation**:
   - Each module must have at least one chapter
   - Module titles must be unique across the book
   - Module IDs must follow the format "module-[number]"

3. **Concept Validation**:
   - Each concept must have a clear, unambiguous definition
   - Concept IDs must be unique across the entire book
   - Each concept must be referenced by at least one chapter

4. **Relationship Validation**:
   - Navigation links must point to valid chapter IDs
   - Related concepts must exist in the system
   - No circular dependencies in concept relationships

## State Transitions (for content review workflow)

### Chapter States
- `draft`: Initial state, content being created
- `review`: Content submitted for review
- `revised`: Feedback incorporated, ready for final review
- `published`: Content approved and published
- `deprecated`: Content no longer relevant

### State Transition Rules
- `draft` → `review`: When author considers content complete
- `review` → `revised`: When reviewer requests changes
- `review` → `published`: When reviewer approves content
- `revised` → `review`: When author makes requested changes
- Any state → `deprecated`: When content becomes outdated