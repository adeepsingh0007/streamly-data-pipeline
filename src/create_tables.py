import psycopg2
from src.sql_queries import create_table_queries, drop_table_queries
from src.config import DB_CONFIG, BASE_DB_CONFIG
import src.logger_config
import logging

def create_database(db_config):
    """
    - Creates and connects to the streamlydb
    - Returns the connection and cursor to streamlydb
    """
    
    # connect to default database
    conn = psycopg2.connect(**BASE_DB_CONFIG)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create streamly database with UTF8 encoding
    try:
        cur.execute("CREATE DATABASE {} WITH ENCODING 'utf8' TEMPLATE template0".format(db_config['dbname']))
    except psycopg2.errors.DuplicateDatabase:
        pass

    # close connection to default database
    conn.close()    
    
    # connect to streamly database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
    conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
    conn.commit()


def main():
    """
    - Drops (if exists) and Creates the streamly database. 
    
    - Establishes connection with the streamly database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    
    logger = logging.getLogger("create_tables")
    logger.info(f"Connecting to {DB_CONFIG['dbname']}...")
    
    conn = None
    
    try:
        cur, conn = create_database(DB_CONFIG)
        
        logger.info("Dropping tables...")
        drop_tables(cur, conn)
        
        logger.info("Creating tables...")
        create_tables(cur, conn)
        
        logger.info("Done!")
    
    except Exception:
        logger.exception("Error creating tables!")
        
        if conn:
            conn.rollback()
    
    finally:    
        if conn:
            conn.close()
        

if __name__ == "__main__":
    main()