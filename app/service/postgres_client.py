import os
import psycopg
from typing import Any


def run_query(
    query: str,
    params: tuple[Any, ...] = (),
    fetch: str | None = None,
):
    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)

            if fetch == "one":
                result = cursor.fetchone()
            elif fetch == "all":
                result = cursor.fetchall()
            else:
                result = None

        connection.commit()
        return result

    finally:
        connection.close()