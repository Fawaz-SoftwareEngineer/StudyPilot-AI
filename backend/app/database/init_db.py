from app.core.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.user import User  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)