import csv
import json
import psycopg2
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

# Read the CSV file and insert data into the database
with open('shows.json', 'r', encoding='utf-8') as csvfile:
    reader = json.loads(''.join(csvfile.readlines()))
    for row in reader:
        #print(row['series_metadata'].replace("'", "\""))
        print(".")
        cursor.execute(
            """
            INSERT INTO shows (
                linked_resource_key, rating, external_id, id, channel_id, type, new, images, promo_title, 
                series_metadata, slug_title, last_public, description, title, slug, promo_description, movie_listing_metadata
            ) VALUES (
                %(linked_resource_key)s, %(rating)s, %(external_id)s, %(id)s, %(channel_id)s, %(type)s, %(new)s, %(images)s, %(promo_title)s, 
                %(series_metadata)s, %(slug_title)s, %(last_public)s, %(description)s, %(title)s, %(slug)s, %(promo_description)s, %(movie_listing_metadata)s
            )
            """,
            {
                'linked_resource_key': str(row['linked_resource_key']),
                'rating': Json(row['rating']),
                'external_id': row['external_id'],
                'id': row['id'],
                'channel_id': row['channel_id'],
                'type': row['type'],
                'new': row['new'],
                'images': Json(row['images']),
                'promo_title': row['promo_title'],
                'series_metadata': Json(row.get('series_metadata', '')),
                'slug_title': row['slug_title'],
                'last_public': row['last_public'],
                'description': row['description'],
                'title': row['title'],
                'slug': row['slug'],
                'promo_description': row['promo_description'],
                'movie_listing_metadata': Json(row.get('movie_listing_metadata', ''))
            }
        )

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
