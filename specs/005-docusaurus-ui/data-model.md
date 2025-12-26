# Data Model: UI Elements and Theme Configuration for Docusaurus UI Upgrade

## Overview
This document defines the data model for UI elements and theme configuration that will be implemented for the Docusaurus UI upgrade. It outlines the structure, properties, and relationships of UI components that will enhance the visual design, navigation, and reading experience.

## Theme Configuration Schema

### Color Palette
```
Primary Colors:
  - primary-base: #1a73e8 (modern blue)
  - primary-light: #4285f4
  - primary-dark: #0d62c9
  - primary-contrast: #ffffff

Secondary Colors:
  - secondary-base: #34a853 (accent green)
  - secondary-light: #5bb974
  - secondary-dark: #2d8743

Neutral Colors:
  - text-primary: #202124
  - text-secondary: #5f6368
  - background-primary: #ffffff
  - background-secondary: #f8f9fa
  - border-color: #dadce0
  - surface-elevation: #ffffff (with shadow)
```

### Typography System
```
Font Stack:
  - heading-font: ['Inter', 'system-ui', 'sans-serif']
  - body-font: ['Inter', 'system-ui', 'sans-serif']
  - code-font: ['Fira Code', 'Consolas', 'monospace']

Scale:
  - h1: 2.5rem (40px) - Hero titles
  - h2: 2rem (32px) - Section headers
  - h3: 1.75rem (28px) - Subsection headers
  - h4: 1.5rem (24px) - Minor headers
  - h5: 1.25rem (20px) - Small headers
  - h6: 1rem (16px) - Label headers
  - body-lg: 1.125rem (18px) - Lead paragraphs
  - body-md: 1rem (16px) - Regular text
  - body-sm: 0.875rem (14px) - Secondary text
  - caption: 0.75rem (12px) - Captions and metadata
```

### Spacing System
```
Spacing Scale (based on 4px base unit):
  - spacing-50: 2px
  - spacing-100: 4px
  - spacing-200: 8px
  - spacing-300: 12px
  - spacing-400: 16px
  - spacing-500: 20px
  - spacing-600: 24px
  - spacing-700: 28px
  - spacing-800: 32px
  - spacing-900: 36px
  - spacing-1000: 40px
  - spacing-1200: 48px
  - spacing-1400: 56px
  - spacing-1600: 64px
```

## UI Component Specifications

### Navigation Components

#### Navbar
```
Properties:
  - height: 64px
  - background: var(--ifm-navbar-background-color)
  - shadow: 0 2px 4px rgba(0,0,0,0.08)
  - padding: 0 spacing-400
  - border-bottom: 1px solid var(--ifm-navbar-border-color)

Elements:
  - logo: 32x32px, left-aligned
  - title: body-md, font-weight: 600
  - navigation-items: space-evenly, min-width: 120px each
  - right-items: icons with spacing-200 between
```

#### Sidebar
```
Properties:
  - width: 280px (desktop), 100% (mobile)
  - background: var(--ifm-sidebar-background-color)
  - border-right: 1px solid var(--ifm-sidebar-border-color)
  - padding: spacing-400 0

Elements:
  - header: padding: spacing-400 spacing-500
  - category:
    - font-weight: 600
    - text-transform: uppercase
    - font-size: 0.75rem
    - letter-spacing: 0.5px
    - padding: spacing-200 spacing-500
  - item:
    - padding: spacing-200 spacing-500
    - border-radius: 6px
    - margin: 0 spacing-200
```

### Content Components

#### Page Layout
```
Properties:
  - max-width: 1200px (content area)
  - padding: spacing-800 spacing-400 (desktop)
  - padding: spacing-600 spacing-300 (mobile)
  - margin: 0 auto
  - background: var(--ifm-background-color)
```

#### Typography Elements
```
Heading Hierarchy:
  - h1:
    - font-size: h1
    - font-weight: 700
    - line-height: 1.2
    - margin: spacing-800 0 spacing-400
  - h2:
    - font-size: h2
    - font-weight: 600
    - line-height: 1.25
    - margin: spacing-700 0 spacing-300
  - h3:
    - font-size: h3
    - font-weight: 600
    - line-height: 1.3
    - margin: spacing-600 0 spacing-200
  - body:
    - font-size: body-md
    - line-height: 1.7
    - margin-bottom: spacing-400
```

#### Code Blocks
```
Properties:
  - background: var(--ifm-code-background)
  - border-radius: 8px
  - padding: spacing-400
  - margin: spacing-400 0
  - border: 1px solid var(--ifm-code-border-color)
  - font-size: 0.875rem

Inline Code:
  - background: var(--ifm-inline-code-background)
  - padding: 0.2em 0.4em
  - border-radius: 4px
  - font-size: 0.875em
```

## Responsive Design Specifications

### Breakpoints
```
- mobile: 0px - 768px
- tablet: 768px - 1024px
- desktop: 1024px+
```

### Mobile Adjustments
```
Sidebar:
  - position: static (not fixed)
  - height: auto
  - border-bottom: 1px solid var(--ifm-sidebar-border-color)

Navbar:
  - height: 56px
  - padding: 0 spacing-300

Typography:
  - h1: 2rem
  - h2: 1.5rem
  - h3: 1.25rem
  - body: 16px
```

## Accessibility Features
```
Color Contrast:
  - Text to background: minimum 4.5:1 ratio
  - Interface elements: minimum 3:1 ratio

Focus Indicators:
  - 2px outline: var(--ifm-color-primary) with 2px offset
  - High contrast mode support

Keyboard Navigation:
  - Tab order follows visual hierarchy
  - Skip to content link available
```

## Theme Configuration Object
```javascript
// Structure for docusaurus.config.js theme modifications
themeConfig: {
  colorMode: {
    defaultMode: 'light',
    disableSwitch: false,
    respectPrefersColorScheme: true
  },
  navbar: {
    style: 'primary',
    hideOnScroll: false,
    title: 'AI-Native Book',
    logo: {
      alt: 'AI-Native Book Logo',
      src: 'img/logo.svg',
    },
    items: [
      // Navigation items configuration
    ]
  },
  footer: {
    style: 'dark',
    links: [],
    copyright: '',
  },
  prism: {
    theme: require('prism-react-renderer').themes.github,
    darkTheme: require('prism-react-renderer').themes.dracula,
    defaultLanguage: 'text',
    additionalLanguages: ['bash', 'python', 'json', 'yaml', 'docker'],
  }
}
```

## CSS Custom Properties (Infima Override)
```css
:root {
  /* Color palette */
  --ifm-color-primary: #1a73e8;
  --ifm-color-primary-dark: #0d62c9;
  --ifm-color-primary-darker: #0c58b9;
  --ifm-color-primary-darkest: #0a4899;
  --ifm-color-primary-light: #4285f4;
  --ifm-color-primary-lighter: #5a95f5;
  --ifm-color-primary-lightest: #84abf7;

  /* Typography */
  --ifm-font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
  --ifm-font-family-monospace: 'Fira Code', Consolas, monospace;
  --ifm-h1-font-size: 2.5rem;
  --ifm-h2-font-size: 2rem;
  --ifm-h3-font-size: 1.75rem;
  --ifm-font-size-base: 1rem;
  --ifm-line-height-base: 1.7;

  /* Spacing */
  --ifm-spacing-vertical: 1rem;
  --ifm-spacing-horizontal: 1rem;

  /* Layout */
  --ifm-container-width: 1200px;
  --ifm-container-width-xl: 1400px;

  /* Code blocks */
  --ifm-code-border-radius: 8px;
  --ifm-code-font-size: 0.875rem;

  /* Sidebar */
  --ifm-menu-color-background-hover: rgba(26, 115, 232, 0.1);

  /* Shadows */
  --ifm-global-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --ifm-global-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```