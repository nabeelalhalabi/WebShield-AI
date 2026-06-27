# WebShield AI

WebShield AI is a full-stack browser-safety platform built as a monorepo. It combines a high-performance FastAPI backend for content analysis with a responsive Manifest V3 browser extension to ensure a safe browsing experience[cite: 2, 16].

## Engineering Philosophy
* **Performance-First:** Models were specifically selected to balance high-accuracy classification with low-latency inference, ensuring real-time page analysis without degrading the user's browsing experience.
* **Resilience:** The system utilizes a fallback mechanism; if neural network models fail to load or timeout, the engine automatically defaults to deterministic heuristic rules to ensure continuous protection[cite: 16, 21].
* **Layered Architecture:** The backend separates model-specific providers from policy and routing logic, allowing for modular updates to detection strategies[cite: 13].

## Core AI Models
* **Text Moderation:** `unitary/toxic-bert` (Toxicity), `facebook/roberta-hate-speech-dynabench-r4-target` (Hate Speech)[cite: 21].
* **Vision Moderation:** `Falconsai/nsfw_image_detection` (NSFW), `jaranohaal/vit-base-violence-detection` (Violence)[cite: 21].
* **Semantic Matching:** `sentence-transformers/all-MiniLM-L6-v2` for interest matching[cite: 21].

## Repository Layout
* `/backend` — FastAPI application, ML model providers, and policy engine[cite: 2].
* `/extension` — Chrome-compatible extension (React, TypeScript, Vite)[cite: 2].
* `/docs` — Technical specifications, architecture, and threat modeling[cite: 2].
* `/shared/contracts` — Interface definitions bridging the backend and extension[cite: 2].

## Quick Start
Please refer to the component-specific guides to run the project locally:
* [Backend Setup Guide](./backend/README.md)
* [Extension Setup Guide](./extension/README.md)