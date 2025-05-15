from sqlalchemy import text
from core.db.database import db
from service.models import SQLqueryResponse

def log_sql_response(resp: SQLqueryResponse) -> None:
    insert_stmt = text(
        """
        INSERT INTO sql_query_log
        (sql_query, success, error_message, rows_returned)
        VALUES (:sql_query, :success, :error_message, :rows_returned)
        """
    )
    with db.engine.begin() as conn:
        conn.execute(
            insert_stmt,
            {
                "sql_query": resp.sql_query,
                "success": resp.success,
                "error_message": resp.error_message,
                "rows_returned": resp.rows_returned,
            },
        )