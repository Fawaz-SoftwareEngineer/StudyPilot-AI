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

# Engineering Decision 004

## Decision

Use a Service Layer architecture.

## Why

- Keeps API routes thin and focused on HTTP.
- Business logic is reusable.
- Easier testing.
- Easier maintenance as the project grows.

# Engineering Decision 005

## Decision

Separate Models, Schemas, Services, and API Routes.

## Why

- Clear separation of responsibilities.
- Prevents business logic from leaking into routes.
- Makes the project easier to navigate.
- Scales well as features increase.

# Engineering Decision 006

## Decision

Track lesson progress separately from course progress.

## Why

- Lessons are the smallest unit of learning.
- Course progress is derived from completed lessons.
- Prevents inconsistent progress calculations.
- Supports future analytics and adaptive learning.

# Engineering Decision 007

## Decision

Store every quiz attempt.

## Why

- Students should be able to review previous attempts.
- Enables learning analytics.
- Makes improvement tracking possible.
- Supports future AI-powered recommendations.

# Engineering Decision 008

## Decision

Reward XP and coins only on the first successful quiz completion.

## Why

- Prevents farming XP by repeating quizzes.
- Encourages genuine learning.
- Keeps progression balanced.
- Makes achievements meaningful.

# Engineering Decision 009

## Decision

Automatically update course progress whenever lesson completion changes.

## Why

- Eliminates manual synchronization.
- Prevents inconsistent data.
- Keeps dashboards accurate.
- Simplifies frontend logic.

# Engineering Decision 010

## Decision

Use UTC for all timestamps.

## Why
- Avoids timezone-related bugs.
- Simplifies deployment worldwide.
- Makes analytics consistent.
- Frontend converts timestamps to local time.

# Engineering Decision 011

## Decision

Store quiz answers for every attempt.

## Why

- Allows detailed quiz review.
- Enables AI feedback in the future.
- Supports analytics on common mistakes.
- Improves learning insights.

# Engineering Decision 012

## Decision

Design the backend as API-first.

## Why

- Backend can serve Web, Android, and iOS clients.
- Easier testing through Swagger/OpenAPI.
- Enables future public APIs.
- Keeps frontend independent of backend implementation.

# Engineering Decision 013

## Decision

Use modular learning hierarchy:
Course → Module → Lesson → Quiz.

## Why

- Mirrors real educational content.
- Allows flexible course organization.
- Supports incremental progression.
- Scales to large learning libraries.

# Engineering Decision 014

## Decision

Use achievements as an educational motivation system rather than an engagement system.

## Why
- Reward meaningful learning milestones.
- Avoid addictive design patterns.
- Reinforce mastery instead of screen time.
- Align with StudyPilot AI's educational philosophy.