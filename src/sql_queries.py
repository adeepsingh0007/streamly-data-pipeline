# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = 'DROP TABLE IF EXISTS users'
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR,
    
    FOREIGN KEY (start_time) REFERENCES time(start_time),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
    );
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
    user_id INT PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR
    );
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration NUMERIC,
    
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
    );
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude NUMERIC,
    longitude NUMERIC
    );
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""INSERT INTO users VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO NOTHING;
""")

song_table_insert = ("""INSERT INTO songs VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT s.song_id songId, a.artist_id artistId
                  FROM songs s
                  JOIN artists a
                  ON s.artist_id = a.artist_id
                  WHERE s.title = %s AND a.name = %s AND s.duration = %s
                  
""")

# QUERY LISTS

create_table_queries = [user_table_create, time_table_create, artist_table_create, song_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]