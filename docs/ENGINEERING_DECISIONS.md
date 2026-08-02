# Engineering Decision 001

## Decision
Build StudyPilot AI with FastAPI, PostgreSQL (Supabase), and SQLAlchemy.

## Why
- FastAPI provides high performance and automatic API documentation.
- PostgreSQL is reliable, scalable, and widely used in production.
- Supabase offers a managed PostgreSQL database with a generous free tier.
- SQLAlchemy provides a robust ORM that keeps our code organized.

## Guiding Principle
We optimize for helping students learn better, not for maximizing time spent in the app.

# Engineering Decision 002

## Decision
Use `pwdlib` for password hashing instead of `passlib`.

## Why
- Better compatibility with modern Python versions.
- Simpler API.
- Actively maintained.
- Recommended by current FastAPI examples.

# Engineering Decision 003

## Decision
Use Argon2 for password hashing.

## Why
- Winner of the Password Hashing Competition (PHC).
- Recommended by modern security guidelines.
- Strong resistance against GPU and ASIC attacks.
- Memory-hard design makes brute-force attacks significantly more expensive.