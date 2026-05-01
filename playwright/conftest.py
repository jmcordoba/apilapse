import sqlite3
import pytest
from playwright.sync_api import Playwright, APIRequestContext


BASE_URL = "http://localhost:8080"
DB_PATH = "../app/db/apilapse.db"


@pytest.fixture(scope="session", autouse=True)
def reset_database():
    """Truncate all tables before the test session to guarantee a clean state."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()
