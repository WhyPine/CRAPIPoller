import json
import psycopg2

dbconnection = psycopg2.connect(
    host="localhost",
    database="Crunchyroll",
    user="postgres",
    password="ADMIN")
cur = dbconnection.cursor()

def NULL_CreateSQLString(s):
    return NULL_CreateString(s.replace("'","''").replace("\n"," "))

def NULL_CreateString(s):
    return "'" + s + "'"

def NULL_GetAttributes(attributes):
    result = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            result += NULL_GetAttributes(value)
        else:
            result.append((attribute, value))
    return result

def NULL_LoadBusinessJSON():
    print("Parsing businesses & categories...")

    # Opening File
    infile = open('./shows.json', 'r')
    shows = json.loads(''.join(infile.readlines()))
    shows_values = []
    for show in shows:
        # Load the JSON data
        print(show.keys())
        # Getting business data
        toInsert = [NULL_CreateSQLString(show['linked_resource_key']),                             # BusinessId
            show['rating'],        # Name
            str(show['external_id']),       # Stars
            str(show['id']),
            str(show['channel_id']),
            str(show['type']),
            bool(show['new']),# ReviewCount
            show['images'],
            str(show['promo_title']),
            show['series_metadata'], 
            str(show['slug_title']),    # Address
            NULL_CreateSQLString(show['last_public']),       # State
            NULL_CreateSQLString(show['description']), 
            str(show['title']),       # City
            str(show['slug']),
            NULL_CreateSQLString(show['promo_description']), # Postalcode
            show.get('movie_listing_metadata', '')]
        shows_values.append('(' + ','.join(toInsert) + ')')
        


    # Inserting business data into the database
    shows_insert = 'INSERT INTO Businesses VALUES ' + ','.join(shows_values) + ';'
    cur.execute(shows_insert)


    # Close file
    infile.close()
    print(business_values.__len__())



def NULL_LoadReviewJSON():
    print("Parsing reviews...")

    # Opening File
    infile = open('./yelp_review.JSON', 'r')
    lines = infile.readlines()
    review_values = []

    for line in lines:
        # Load the JSON data
        data = json.loads(line)
        
        # Getting review data
        toInsert = [NULL_CreateString(data['review_id']),    # ReviewId
                    NULL_CreateString(data['user_id']),      # UserId
                    NULL_CreateString(data['business_id']),  # BusinessId
                                  str(data['stars']),        # Stars
                    NULL_CreateString(data['date']),         # Date
                    NULL_CreateSQLString(data['text'])]      # Text  
        
        review_values.append('(' + ','.join(toInsert) + ')')
        
    # Inserting review data into the database
    review_insert = 'INSERT INTO Reviews VALUES ' + ','.join(review_values) + ';'
    cur.execute(review_insert)

    # Close file
    infile.close()
    print(review_values.__len__())


def NULL_LoadUserJSON():
    print("Parsing users...")

    # Opening File
    infile = open('./yelp_user.JSON', 'r')
    lines = infile.readlines()
    user_values = []

    for line in lines:
        # Load the JSON data
        data = json.loads(line)

        # Getting user data
        toInsert = [NULL_CreateString(data['user_id']), 
                    NULL_CreateSQLString(data['name'])]
        user_values.append('(' + ','.join(toInsert) + ')')
        
    # Inserting user data into the database
    user_insert = 'INSERT INTO Users VALUES ' + ','.join(user_values) + ';'
    cur.execute(user_insert)

    # Close file
    infile.close()
    print(user_values.__len__())

def NULL_LoadCheckinJSON():
    print("Parsing checkins...")

    # Opening File
    infile = open('./yelp_checkin.JSON', 'r')
    lines = infile.readlines()
    checkins_values = []
    
    for line in lines:
        # Load the JSON data
        data = json.loads(line)

        for (day, time) in data['time'].items():
            for (hour, count) in time.items():
                # Getting checkin data
                ToPrint = [NULL_CreateString(data['business_id']), # businessid
                           NULL_CreateString(day),                 # Day
                           NULL_CreateString(hour),                # Time
                           str(count)]                             # Count
                checkins_values.append('(' + ','.join(ToPrint) + ')')
    
    # Inserting checkin data into the database
    checkins_insert = 'INSERT INTO Checkins VALUES ' + ','.join(checkins_values) + ';'
    cur.execute(checkins_insert)

    # Close file
    infile.close()
    print(checkins_values.__len__())


NULL_LoadBusinessJSON()
NULL_LoadUserJSON()
NULL_LoadCheckinJSON()
NULL_LoadReviewJSON()

cur.close()
dbconnection.commit()
dbconnection.close()