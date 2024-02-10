import csv
from psycopg2 import sql
import ast
from db_conn import connect


conn = connect()

cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS filters (
        movie_id INTEGER PRIMARY KEY,
        idx INTEGER,
        adult BOOLEAN,
        genres TEXT[],
        original_language VARCHAR,
        production_countries TEXT[],
        release_year INTEGER,
        vote_average FLOAT,
        popularity_category VARCHAR
    );
"""
)
conn.commit()

with open("../Filtered_Data/db_filters.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for i, row in enumerate(reader):
        row[2] = ast.literal_eval(row[2])
        row[4] = ast.literal_eval(row[4])

        cur.execute(
            sql.SQL(
                """
            INSERT INTO filters (movie_id, idx, adult, genres, original_language, production_countries, release_year, vote_average, popularity_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
            ),
            (row[0], i, row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
        )
        print(i)

conn.commit()

cur.close()
conn.close()
