# Backend architecture

The backend follows a layered layout:

- `api/` for HTTP routes and dependency wiring
- `presentation/` for transport schemas and mappers
- `application/` for orchestrated use cases
- `domain/` for entities, policy, scoring, and rules
- `infrastructure/` for model providers, detectors, storage, and external adapters

Pretrained models are wrapped in provider classes and consumed through detector classes. This keeps model-specific code isolated from policy and routing code.
