import logging

logger = logging.getLogger(__name__)

TABLE_NAME = "youtube_api"
STAGING_SCHEMA = "staging"
CORE_SCHEMA = "core"


def insert_rows(cursor, connection, schema, row):
    try:
        if schema == STAGING_SCHEMA:
            video_id = row["video_id"]
            logger.info(f"inserting video_id {video_id} into {schema}.{TABLE_NAME}")
            insert_sql = f"""
            INSERT INTO {schema}.{TABLE_NAME} (
                video_id, title, published_at, duration,
                view_count, like_count, comment_count
            )
            VALUES (
                %(video_id)s, %(title)s, %(published_at)s, %(duration)s,
                %(view_count)s, %(like_count)s, %(comment_count)s
            )
            """
            cursor.execute(insert_sql, row)
            connection.commit()
        else:
            video_id = row["video_id"]
            logger.info(f"Inserting video_id {video_id} into {schema}")
            insert_sql = f"""
            INSERT INTO {schema}.{TABLE_NAME} (
                video_id, title, published_at, duration, video_type,
                view_count, like_count, comment_count
            )
            VALUES (
                %(video_id)s, %(title)s, %(published_at)s, %(duration)s, %(video_type)s,
                %(view_count)s, %(like_count)s, %(comment_count)s
            )
            """
            cursor.execute(insert_sql, row)
            connection.commit()
    except Exception as e:
        logger.error(f"Error inserting row into {schema}.{TABLE_NAME}: {e}")
        raise


def update_rows(cursor, connection, schema, row):
    try:
        if schema == STAGING_SCHEMA:
            video_id = row["video_id"]
            logger.info(f"Updating video_id {video_id} in {schema}.{TABLE_NAME}")
            update_sql = f"""
            UPDATE {schema}.{TABLE_NAME}
            SET title = %(title)s,
                view_count = %(view_count)s,
                like_count = %(like_count)s,
                comment_count = %(comment_count)s
            WHERE video_id = %(video_id)s
            AND published_at = %(published_at)s
            """
            cursor.execute(update_sql, row)
            connection.commit()
        else:
            video_id = row["video_id"]
            logger.info(f"Updating video_id {video_id} in {schema}.{TABLE_NAME}")
            update_sql = f"""
            UPDATE {schema}.{TABLE_NAME}
            SET title = %(title)s,
                view_count = %(view_count)s,
                like_count = %(like_count)s,
                comment_count = %(comment_count)s
            WHERE video_id = %(video_id)s
            AND published_at = %(published_at)s
            """
            cursor.execute(update_sql, row)
            connection.commit()
    except Exception as e:
        logger.error(f"Error updating row in {schema}.{TABLE_NAME}: {e}")
        raise


def delete_rows(cursor, connection, schema, ids_to_delete):
    try:
        ids_str = ", ".join([f"'{id}'" for id in ids_to_delete])
        delete_sql = f"""
        DELETE FROM {schema}.{TABLE_NAME}
        WHERE video_id IN ({ids_str})
        """
        logger.info(f"Deleting video_ids {ids_to_delete} from {schema}.{TABLE_NAME}")
        cursor.execute(delete_sql)
        connection.commit()
    except Exception as e:
        logger.error(f"Error deleting rows from {schema}.{TABLE_NAME}: {e}")
        raise
