# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2024-16-15

### Added

- Google OAuth2 integration for user authentication
- Google callback endpoint for handling OAuth flow
- User authentication with Google credentials
- Session middleware for managing OAuth state
- Frontend redirect URL support for OAuth callback

### Changed

- Enhanced user authentication flow to support both password and Google login
- Updated authentication response schemas to include user data
- Improved error handling for OAuth authentication

## [0.1.0] - 2024-09-15

### Added

- Initial release of Kwiki AI Backend
- FastAPI application setup with OpenAPI documentation
- PostgreSQL database integration with SQLAlchemy
- User authentication with JWT tokens
- Flashcard deck generation using Groq LLM
- CRUD operations for flashcard decks
- Rate limiting for API endpoints
- Logging system with rotation
- Alembic migrations for database schema
- CI pipeline with GitHub Actions
- Unit testing setup with pytest
- CORS middleware configuration
- Basic security measures and password hashing
- Documentation and API endpoints