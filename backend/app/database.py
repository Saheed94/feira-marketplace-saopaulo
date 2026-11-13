import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use the environment variable if it exists, otherwise fall back to the hardcoded local URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://feira_admin:feira_dev_password@localhost:5432/feira_marketplace"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base


# DATABASE_URL = (
#     "postgresql+psycopg2://"
#     "feira_admin:"
#     "feira_dev_password"
#     "@localhost:5432/"
#     "feira_marketplace"
# )


# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )


# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )


# Base = declarative_base()


# def get_db():
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


