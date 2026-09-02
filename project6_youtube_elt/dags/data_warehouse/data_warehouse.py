import logging
from airflow.decorators import task

from data_warehouse.data_utils import (
    get_connection,
    close_connection,
    create_schema,
    create_table,
    get_video_ids,
)
from data_warehouse.data_loading import load_data
from data_warehouse.data_modification import insert_rows, update_rows, delete_rows
from data_warehouse.data_transformation import transform_data

logger = logging.getLogger(__name__)

@task
def staging_table():
    schema = "staging"
    connection = None
    cursor = None
    try:
        connection, cursor = get_connection()
        raw_data = load_data()
        create_schema(schema)
        create_table(schema)
        table_ids = get_video_ids(cursor, schema)
        for row in raw_data:
            if len(table_ids) == 0:
                insert_rows(cursor,connection, schema, row)
            else:
                if row["video_id"] in table_ids:
                    update_rows(cursor, connection, schema, row)
                else:
                    insert_rows(cursor,connection, schema, row)
        ids_in_json ={row["video_id"] for row in raw_data}
        ids_to_delete = set(table_ids) - ids_in_json
        if ids_to_delete:
            delete_rows(cursor, connection, schema, ids_to_delete)
        logger.info(f"Successfully updated {schema} table")
    except Exception as e:
        logger.error(f"Error updating {schema} table: {e}")
        raise
    finally:
        if connection is not None and cursor is not None:
            close_connection(connection,cursor)

@task
def core_table():
    schema = "core"        
    connection = None
    cursor = None
    current_video_ids = set()
    try:
        connection, cursor = get_connection()
        create_schema(schema)
        create_table(schema)
        table_ids = get_video_ids(cursor,schema)
        cursor.execute(f"SELECT * FROM staging.youtube_api")
        staging_data = cursor.fetchall()
        for row in staging_data:
            transformed_row = transform_data(row)
            current_video_ids.add(transformed_row["video_id"])

            if len(table_ids) == 0:
                insert_rows(cursor, connection, schema, transformed_row)
            else:
                if transformed_row["video_id"] in table_ids:
                    update_rows(cursor,connection,schema,transformed_row)
                else:
                    insert_rows(cursor, connection, schema, transformed_row)
        ids_to_delete = set(table_ids) - current_video_ids
        if ids_to_delete:
            delete_rows(cursor, connection, schema, ids_to_delete)
        logger.info(f"Successfully updated {schema} table")
    except Exception as e:
        logger.error(f"Error updating {schema} table: {e}")
        raise
    finally:
        if connection is not None and cursor is not None:
            close_connection(connection, cursor)