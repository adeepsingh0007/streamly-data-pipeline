import os
import glob
import psycopg2
import pandas as pd
from src.sql_queries import artist_table_insert, song_table_insert, time_table_insert, user_table_insert, songplay_table_insert, song_select
from src.config import DB_CONFIG
import src.logger_config
import logging

def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.dayofweek)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, list(row))

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func, logger):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    logger.info('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        logger.info('{}/{} files processed.'.format(i, num_files))


def main():
    
    logger = logging.getLogger("etl")
    logger.info("Starting ETL...")
    logger.info("Obtaining database connection...")
    conn = None
    
    try:          
        #connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        logger.info("Processing song data...")
        
        #process song data
        process_data(cur, conn, filepath='data/song_data', func=process_song_file, logger=logger)
        logger.info("Song data successfully loaded into database!")
        
        logger.info("Processing log data...")
        
        #process log data
        process_data(cur, conn, filepath='data/log_data', func=process_log_file, logger=logger)
        logger.info("Log data successfully loaded into database!")
        
        logger.info("ETL successful!")
           
    except Exception:
        logger.exception("Error occurred.")
        if conn:
            conn.rollback()
    
    finally:        
        #closing database connection
        logger.info("Closing database connection...")
        if conn:
            conn.close()

if __name__ == "__main__":
    main()