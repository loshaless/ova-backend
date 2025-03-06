from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Connection string for Google Cloud SQL PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# For Google Cloud SQL with Cloud SQL Auth Proxy
# DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?unix_sock=/cloudsql/INSTANCE_CONNECTION_NAME/.s.PGSQL.5432"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,               # Maximum number of permanent connections
    max_overflow=10,           # Maximum number of connections that can be created beyond pool_size
    pool_timeout=30,           # Seconds to wait before giving up on getting a connection from the pool
    pool_recycle=1800,         # Recycle connections after 1800 seconds (30 minutes)
    pool_pre_ping=True         # Issue a test ping before using a connection
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()