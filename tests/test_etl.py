from src.etl import process_song_file, process_log_file, process_data
import logging

def test_database_schema(test_db):
    cur, conn = test_db

    expected_tables = {
        "songplays",
        "users",
        "songs",
        "artists",
        "time"
    }

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    actual_tables = {row[0] for row in cur.fetchall()}

    assert expected_tables.issubset(actual_tables)

def test_process_song_file(test_db):
    cur, conn = test_db

    filepath = "data/song_data/A/A/A/TRAAAAW128F429D538.json"

    process_song_file(cur, filepath)
    conn.commit()

    cur.execute(
        "SELECT song_id, title FROM songs WHERE song_id = %s",
        ("SOMZWCG12A8C13C480",)
    )

    result = cur.fetchone()

    assert result == (
        "SOMZWCG12A8C13C480",
        "I Didn't Mean To"
    )
    
def test_process_log_file(test_db):
    cur, conn = test_db

    filepath = "data/log_data/2018/11/2018-11-01-events.json"

    process_log_file(cur, filepath)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM time")
    time_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    assert time_count > 0
    assert user_count > 0
    
def test_etl_pipeline(test_db):
    cur, conn = test_db
    logger = logging.getLogger("test_etl")

    process_data(
        cur,
        conn,
        "data/song_data",
        process_song_file,
        logger
    )

    process_data(
        cur,
        conn,
        "data/log_data",
        process_log_file,
        logger
    )

    cur.execute("SELECT COUNT(*) FROM songs")
    song_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM songplays")
    songplay_count = cur.fetchone()[0]

    assert song_count > 0
    assert songplay_count > 0