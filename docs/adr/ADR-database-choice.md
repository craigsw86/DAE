# Title
- Use SQLite for local development.

## Context
- We needed a lightweight database that works offline for testing.

## Decision
- We chose SQLite for local development.

### Rationale
- Simplicity and Convenience.
- Fewer Dependencies.
- Faster Development Speed.
- Better Portability.
- Better for Troubleshooting Issues.

### Alternatives Considered
- PostgreSQL (more powerful, but heavier)

### Consequences
- It is enough for this project, which does not hold or process any PII or PHI.

## References
- https://www.sqlite.org 