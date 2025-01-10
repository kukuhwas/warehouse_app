import pytest
from core.database import connect_to_db

@pytest.fixture(scope="module")
def db_connection():
    conn = connect_to_db(environment="development") # connect_to_db untuk development
    yield conn
    conn.close()
