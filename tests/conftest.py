import pytest

from src.config import TEST_DB_CONFIG
from src.create_tables import create_database, drop_tables, create_tables

@pytest.fixture
def test_db():
    cur, conn = create_database(TEST_DB_CONFIG)
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    
    yield cur, conn
    
    conn.close()