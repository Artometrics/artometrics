# Artometrics Master Manual: Web Architecture and Design System

Document ID: ART-WEB-ARCH-001  
Version: 2.0  
Classification: Internal Engineering Standard  
Author: Artometrics Platform & Engineering Team  

---

## 1. Executive Summary

Artometrics is a unified cross-platform publishing and analytics platform engineered with Expo (React Native Web + native runtimes). It delivers a publication aesthetic with real-time reactive charting, an ambient moving shoegaze theme engine, tactile morphic elevation boxes, and server-side static search engine optimization (AEO/SEO).

This document establishes the official engineering standard for how web systems, components, shaders, and styling pipelines are architected, authored, and maintained across the Artometrics ecosystem.

---

## 2. Core Technology Stack

Artometrics avoids fragmented codebases (such as separate Next.js and React Native apps) by employing a single, universal Expo architecture:

```
[Content Layer: Markdown/MDX + Quarto QMD]
                  │
                  ▼
[Build Pipeline: Node.js scripts/build-content.mjs]
                  │
                  ▼
[Static Cache: src/generated/*.json]
                  │
                  ▼
[Universal Client: Expo 57 + Expo Router]
   ├── Web Tier: React Native Web (Static HTML Export via `expo export -p web`)
   └── Native Tier: iOS / Android (React Native Bridgeless Architecture)
```

### 2.1 Framework and Router
- **Runtime**: Expo SDK 57 with React 19.
- **Routing**: Expo Router (file-based routing under `app/`).
  - Layout chrome: `app/(site)/_layout.tsx` wraps all consumer-facing routes with `ThemeProvider`, `ChromeProvider`, navigation bars, and background stages.
  - Slug handler: `app/(site)/[slug].tsx` dynamically hydrates report articles from static JSON payloads.
  - Universal Static Generation: Output generated via `expo export -p web` directly to `dist/`, served through Netlify with zero-cold-start edge delivery.

### 2.2 Styling and Utility Engine
- **Tailwind / Uniwind**: Utility-first atomic styling compiled ahead of time (`lib/uniwind-theme.ts`).
- **Global Theme & Shaders**: `public/css/shoegaze-theme.css` manages hardware-accelerated animated canvases, fluid SVG noise grain, and tactile elevation box-shadows.
- **Editorial Typography Engine**: `public/css/artometrics-article.css` governs centered magazine reading typography, drop-caps, citations, and interactive chart wrappers.

---

## 3. The Shoegaze 3D Lava-Lamp Background Engine

The Artometrics visual identity pairs high-rigor data journalism with a dreamy, tactile "shoegaze" dream-pop atmosphere (drawing aesthetic lineage from analog vinyl textures, My Bloody Valentine album covers, and optical stereoscopic 3D glasses).

### 3.1 Color Theory: 3D Glasses & Slurpee Palette
The ambient environment leverages anaglyph stereoscopic chromatic tension:
- **Cherry Red (`#E60000`)**: High-saturation hot crimson, representing intensity, risk, and anomaly detection.
- **Cobalt Blue (`#3367E7`)**: Deep electric blue raspberry, representing baseline stability, institutional authority, and verification.
- **Deep Void Background (`#06070B` in Dark Mode, `#F8F8F5` in Light Mode)**: Pure dark indigo-black obsidian or tactile warm archival paper.

### 3.2 Drifting Fluid Mesh (Lava Lamp Physics)
The background consists of four continuous, out-of-phase orbital nodes defined in `components/ShoegazeBackground.tsx` and styled in `public/css/shoegaze-theme.css`:
- **Node 1 (Cherry Red)**: 75vw radial orb with 26-second easing cycle.
- **Node 2 (Electric Cobalt)**: 85vw radial orb with 32-second counter-diagonal easing cycle.
- **Node 3 (Violet/Indigo Blend)**: 60vw center flare with 22-second pulse cycle.
- **Node 4 (Cyan Ice Glint)**: 50vw perimeter glint with 28-second lateral orbital sweep.

Every node is rendered with heavy Gaussian diffusion (`filter: blur(85px)` to `blur(110px)`) and hardware-accelerated with `transform: translate3d(0, 0, 0)` and `will-change: transform`. On screens configured with `prefers-reduced-motion: reduce`, keyframes are automatically suspended while preserving the static atmospheric glow.

### 3.3 Analog Noise Grain Synthesis
Digital gradients frequently suffer from 8-bit color quantization banding. Artometrics eliminates banding and introduces an authentic tactile vinyl fuzz by overlaying an inline SVG `feTurbulence` filter:

```xml
<svg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'>
  <filter id='grainFilter'>
    <feTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='3' stitchTiles='stitch'/>
    <feColorMatrix type='matrix' values='1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.22 0'/>
  </filter>
  <rect width='100%' height='100%' filter='url(#grainFilter)' opacity='1'/>
</svg>
```

This pattern repeats across the viewport with `mix-blend-mode: overlay` (in dark mode) or `multiply` (in light mode), generating organic film grain with zero network requests or image asset payloads.

---

## 4. Tactile Floating Box & Drop Shadow System

Artometrics rejects flat, lifeless corporate UI in favor of tactile physical elevation, crisp geometric edges, and morphic highlights.

### 4.1 Card Anatomy
Each stat box and callout card features a structured four-part layout:
1. **Category Pill Badge**: Positioned at the top right, featuring monospace typography (`DM Mono`), high-contrast pill styling, and color-coded status badges (`Financial Risk`, `Mandatory Scope`, `Market Opportunity`, `Dataset Scale`).
2. **Hero Metric**: Large display numerals (Anton / DM Sans) set in electric blue (`#3367E7`) or cherry red (`#E60000`).
3. **Narrative Finding**: DM Sans body text delivering an objective editorial summary.
4. **Citation Anchor**: A bottom-aligned citation with an external link arrow (`↗`).

### 4.2 Elevation Specifications
- **Light Theme Box Shadow**:
  `box-shadow: 0 10px 0 #0A0A0A, 0 16px 28px -6px rgba(0, 0, 0, 0.16);`
- **Dark Theme Box Shadow**:
  `box-shadow: 0 10px 0 #000000, 0 18px 32px -4px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(51, 103, 231, 0.15);`
- **Interactive Morphic Hover State**:
  Upon cursor hover, cards translate `translateY(-3px)`, the drop shadow expands to `14px`, and the border receives an intensified 3D glow highlight (`rgba(107, 148, 255, 0.45)`).

---

## 5. Charting and Data Visualization System

Artometrics implements a dual-target charting architecture:
1. **Interactive Web Hydration**: In `components/ArticleBody.web.tsx`, chart containers detect `<div class="art-chart-live" data-chart-src="...">` tags, loading Plotly.js dynamically to render responsive scatter plots, violin charts, and heatmaps.
2. **Headless Static PNG Fallback**: Pre-rendered PNG snapshots (`articles/<slug>/charts/*.png`) are served immediately during the initial page paint and for native iOS/Android devices, eliminating chart layout shifts.
3. **Container Floating Elevation**: In `artometrics-article.css`, all `.art-chart` containers are wrapped in floating tactile cards with 16px border-radius, dark offset drop-shadows, and semi-translucent glass surfaces.

---

## 6. Engineering Conventions and Quality Checklist

1. **Zero Emojis**: All code, markup, stylesheets, metadata, and user-facing copy must strictly avoid emojis. Standard ASCII glyphs or typography symbols (such as `↗`, `—`, `·`) are preferred.
2. **Path Aliases**: All application imports must use the `@/` project root alias (for example, `import { useTheme } from "@/lib/theme";`).
3. **Static Export Integrity**: Every change to routes, components, or layout must pass `npm run build` (`expo export -p web`) without runtime compilation errors.
4. **Contrast Compliance**: Text elements rendered above ambient animated gradients must maintain WCAG AAA contrast ratios.
