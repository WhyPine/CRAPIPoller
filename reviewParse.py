import csv
import json
import psycopg2
from psycopg2.extras import Json
from client import CrunchyrollClient
import methods
from psycopg2.extras import Json


# Database connection parameters
DB_NAME = "Crunchyroll"
DB_USER = "postgres"
DB_PASS = "ADMIN"
DB_HOST = "localhost"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST
)
cursor = conn.cursor()

client = CrunchyrollClient("goodingaidan@gmail.com",  "Sx/6@SBzk&.ghKP")
client.auth()

# Read the CSV file and insert data into the database
cursor.execute("SELECT linked_resource_key FROM shows;")
shows = cursor.fetchall()
for show in shows:
    seriesID = show[0].split("/")[2]
    reviews = methods.listSeriesReviews(client, seriesID, page_size=20)
    print("---------")
    for review in reviews:
        #print(row['series_metadata'].replace("'", "\""))
        cursor.execute(
            """
            INSERT INTO reviews (
            series_id, review_id, title, body, language, created_at, modified_at, authored_reviews, spoiler, 
            author_rating, author, ratings, reported
            ) VALUES (
                %(series_id)s, %(review_id)s, %(title)s, %(body)s, %(language)s, %(created_at)s, %(modified_at)s, %(authored_reviews)s, %(spoiler)s, 
                %(author_rating)s, %(author)s, %(ratings)s, %(reported)s
            )
            """,
            {
                'series_id' : seriesID,
                'review_id': review['review']['id'],
                'title': review['review']['title'],
                'body': review['review']['body'],
                'language': review['review']['language'],
                'created_at': review['review']['created_at'],
                'modified_at': review['review']['modified_at'],
                'authored_reviews': review['review']['authored_reviews'],
                'spoiler': review['review']['spoiler'],
                'author_rating': review['author_rating'],
                'author': Json(review['author']),
                'ratings': Json(review['ratings']),
                'reported': review['reported']
            }
        )

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
