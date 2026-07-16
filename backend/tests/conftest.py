"""
Test configuration — uses a separate SQLite file-based database.
Each test gets a fully isolated session via nested transactions (savepoints).
After each test the savepoint is rolled back, leaving the DB clean for the next test.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

# Patch settings before any app import
os.environ.setdefault("DATABASE_URL", TEST_DB_URL)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-tests-only")
os.environ.setdefault("GOOGLE_API_KEY", "fake-key-for-tests")

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DB_URL else {},
)

# Enable SQLite savepoint support (needed for nested transactions)
if "sqlite" in TEST_DB_URL:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA journal_mode=WAL")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create all tables once per session, drop them when done."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(setup_db):
    """
    Provide a test database session that is rolled back after every test.

    Pattern:
      1. Open a connection and begin an outer transaction.
      2. Bind a session to that connection.
      3. For each ORM flush/commit inside the test, use a SAVEPOINT so the
         session thinks it committed but the outer transaction is still open.
      4. After the test, roll back the outer transaction — the DB is pristine.
    """
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    # Intercept commits and convert them to savepoint releases so data is
    # visible within the test but never actually committed to the DB.
    if "sqlite" in TEST_DB_URL:
        # SQLite nested transactions via savepoints
        from sqlalchemy import event as sa_event

        @sa_event.listens_for(session, "after_transaction_end")
        def restart_savepoint(sess, trans):
            if trans.nested and not trans._parent.nested:
                sess.begin_nested()

        session.begin_nested()  # open the first savepoint

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    """TestClient whose get_db dependency is overridden with the test session."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()
