# Karaoke-Inator: Agent Guidelines

This document provides essential guidance for agentic coding agents operating on this repository.

## Project Structure

Karaoke-Inator is a distributed microservices application for processing YouTube audio:

- **Frontend** (`services/frontend/`): React + React Router 7, TypeScript
- **Orchestrator Service** (`services/orchestrator-service/`): FastAPI (Python 3.12), main gateway
- **Song Management Service** (`services/song-management-service/`): FastAPI (Python 3.12), PostgreSQL
- **Lyrics Extraction Service** (`services/lyrics-extraction-service/`): FastAPI (Python 3.10)
- **Voice Separation Service** (`services/voice-separation-service/`): FastAPI (Python 3.10)

## Build & Test Commands

### Frontend (TypeScript/React)

```bash
# Navigate to frontend directory
cd services/frontend

# Install dependencies
npm install

# Development server
npm run dev

# Type checking
npm run typecheck

# Linting
npm run lint
npm run lint:fix

# Format code
npm run format

# Build for production
npm build

# Generate API clients from OpenAPI specs
npm run client-gen

# Generate AsyncAPI models from WebSocket spec
npm run asyncapi-gen
```

### Python Services (FastAPI)

All Python services use `uv` package manager and Pyright for type checking.

```bash
# Navigate to service directory (e.g., orchestrator-service)
cd services/[service-name]

# Install dependencies
uv sync

# Run service
uv run python main.py

# Type check
uv run pyright .

# Code formatting/linting with Ruff (if configured)
uv run ruff check .
uv run ruff format .
```

## Code Style Guidelines

### TypeScript/React (Frontend)

**Imports:**
- Use path aliases: `~/*` for app root, `@/api/*` for API modules
- Group imports: external libraries, then internal modules
- Use ES modules (`import`/`export`)
- Example: `import { Button } from "~/components/Button"`

**Formatting:**
- Line width: 100 characters
- Indentation: 2 spaces
- Quotes: double quotes for strings
- Semicolons: required
- Trailing commas: ES5 style (objects/arrays, not function params)
- Arrow function parens: always `(x) => x`

**Naming Conventions:**
- Components: PascalCase (`Button.tsx`, `UserProfile.tsx`)
- Files: kebab-case or PascalCase (match component name)
- Functions/variables: camelCase
- Constants: UPPER_SNAKE_CASE
- React Router route files: follow file-based routing convention (`_app.search.tsx`)

**Types:**
- Use strict TypeScript (`strict: true` in tsconfig.json)
- Explicit return types on functions and components
- No `any` type; use `unknown` if necessary with type guards
- Use Pydantic-generated types for API responses

**Error Handling:**
- Wrap async operations in try/catch
- Log errors with context
- Return user-friendly error messages in UI
- Use React Query for server state with built-in error handling

**React Patterns:**
- Use React Router 7 for routing
- Use React Query (`@tanstack/react-query`) for data fetching
- Components should be functional, not class-based
- Extract reusable components to `~/components/`

**Linting Rules:**
- No unused variables (auto-ignore with `_` prefix: `const _unused = value`)
- No explicit `any` (warn level)
- No console logs except `.warn()` and `.error()`
- Prettier integration enforces formatting

### Python (FastAPI Services)

**Imports:**
- Standard library imports first
- Third-party imports second
- Local imports last
- Use absolute imports: `from services.auth import verify_token`
- Organize alphabetically within groups

**Formatting:**
- Line length: follow Ruff defaults (88 characters recommended)
- Indentation: 4 spaces
- Type hints: required on all functions
- Use `from __future__ import annotations` for forward references

**Naming Conventions:**
- Classes: PascalCase (`UserService`, `ProcessingResult`)
- Functions/variables: snake_case (`get_user`, `is_valid`)
- Constants: UPPER_SNAKE_CASE
- Private methods: prefix with `_` (`_internal_helper`)
- Route handlers: descriptive names reflecting HTTP method and resource

**Types:**
- Pyright strict mode enabled: `typeCheckingMode = "strict"`
- All function parameters and returns require type hints
- Use Pydantic models for request/response validation
- Use `Optional[T]` for nullable values, not `Union[T, None]`
- Generic types: `List[str]`, `Dict[str, Any]`, `Tuple[int, ...]`

**Error Handling:**
- Define custom exception classes inheriting from `Exception`
- Raise exceptions with descriptive messages
- Use FastAPI `HTTPException` for API errors with appropriate status codes
- Log all errors: `logger.error(f"Operation failed: {e}")`
- Provide meaningful error responses to clients

**Async/Await:**
- Use async functions for I/O operations (database, HTTP calls)
- Use `asyncio` for concurrent operations
- Prefix async functions with `async def`
- Always `await` async calls, don't fire-and-forget

**FastAPI Patterns:**
- Define routes in separate router modules in `routes/` directory
- Use dependency injection with Dishka (`@inject` decorator)
- Validate requests with Pydantic models
- Return Pydantic models in responses
- Document endpoints with docstrings and OpenAPI annotations

**Testing:**
- Use pytest for unit tests (installed in client pyproject.toml)
- Tests go in `tests/` directory mirroring source structure
- Use async test fixtures for async code
- Mock external service calls

## Key Dependencies

**Frontend:**
- React Router 7 (routing)
- React Query (server state management)
- Tailwind CSS (styling)
- TypeScript (type safety)
- Prettier + ESLint (formatting/linting)

**Python Services:**
- FastAPI (web framework)
- Pydantic 2 (validation)
- SQLAlchemy 2 (ORM, for song-management-service)
- Pyright (type checking)
- Ruff (linting/formatting)
- Dishka (dependency injection)
- httpx (async HTTP client)
- yt-dlp (YouTube audio download)

## Important Notes

- **Environment Variables**: Each service has `.env.example` - copy to `.env` for local development
- **Python Version**: Orchestrator requires Python 3.12, other services vary (check pyproject.toml)
- **Package Manager**: Python uses `uv` (faster than pip)
- **Type Checking**: Required before commits - run `uv run pyright .` for Python services
- **Generated Code**: Do not edit `clients/` directories - these are auto-generated from OpenAPI specs

## Common Issues

- Frontend tests/vitest not configured: use `npm run typecheck` for type safety instead
- Python import errors: ensure you're running commands with `uv run` in the correct service directory
- Service discovery: all services expose OpenAPI specs at `/openapi.json`
