from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

BASE_DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("BASE_DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

TEST_DB_CONFIG = DB_CONFIG.copy()
TEST_DB_CONFIG["dbname"] = os.getenv("TEST_DBNAME")