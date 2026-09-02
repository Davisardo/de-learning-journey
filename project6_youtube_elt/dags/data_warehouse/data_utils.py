from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

TABLE_NAME = "youtube_api"


def get_connection():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", schema="elt_db")
    connection = hook.get_conn()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_schema(schema):
    connection, cursor = get_connection()
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema}"
    cursor.execute(schema_sql)
    connection.commit()
    close_connection(connection, cursor)


def create_table(schema):
    connection, cursor = get_connection()
    if schema == "staging":
        table_sql = f"""
        CREATE TABLE IF NOT EXISTS staging.{TABLE_NAME} (
            video_id VARCHAR(11) PRIMARY KEY,
            title TEXT,
            published_at TEXT,
            duration VARCHAR(20),
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER
        )
        """
    else:
        table_sql = f"""
        CREATE TABLE IF NOT EXISTS core.{TABLE_NAME} (
            video_id VARCHAR(11) PRIMARY KEY,
            title TEXT,
            published_at TEXT,
            duration INTEGER,
            video_type VARCHAR(20),
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER
        )
        """
    
    cursor.execute(table_sql)
    connection.commit()
    close_connection(connection, cursor)

def get_video_ids(cursor, schema):
    query =f"SELECT video_id FROM {schema}.{TABLE_NAME}"
    cursor.execute(query)
    rows = cursor.fetchall()
    video_ids = [row["video_id"] for row in rows]
    return video_ids
