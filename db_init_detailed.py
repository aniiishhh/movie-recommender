import csv
from psycopg2 import sql
import ast
from db_conn import connect


conn = connect()

cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS detailed (
        id INTEGER PRIMARY KEY,
        idx INTEGER,
        overview TEXT,
        popularity FLOAT,
        production_companies TEXT[],
        production_countries TEXT[],
        release_date DATE,
        runtime FLOAT,
        tagline TEXT,
        vote_average FLOAT,
        vote_count FLOAT,
        release_year FLOAT,
        revised_title VARCHAR,
        keywords TEXT[],
        casts TEXT[],
        crew TEXT[],
        poster_path VARCHAR
    );
"""
)
conn.commit()

with open(
    "../Filtered_Data/cropped_full.csv", "r", newline="", encoding="utf-8"
) as file:
    reader = csv.reader(file)
    next(reader)
    for i, row in enumerate(reader):
        row[9] = ast.literal_eval(row[9])
        row[8] = ast.literal_eval(row[8])
        row[19] = ast.literal_eval(row[19])
        row[20] = ast.literal_eval(row[20])
        row[21] = ast.literal_eval(row[21])

        cur.execute(
            sql.SQL(
                """
            INSERT INTO detailed (
                id, idx, overview, popularity, production_companies,
                production_countries, release_date, runtime, tagline, vote_average, vote_count,
                release_year, revised_title, keywords, casts, crew, poster_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
            ),
            (
                row[3],
                i,
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11],
                row[13],
                row[15],
                row[16],
                row[17],
                row[18],
                row[19],
                row[20],
                row[21],
                row[22],
            ),
        )
        if i % 1000 == 0:
            print(i)

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
