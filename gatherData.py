from client import CrunchyrollClient
import json
import pandas as pd
import methods

def main():
    client = CrunchyrollClient("goodingaidan@gmail.com",  "Sx/6@SBzk&.ghKP")
    client.auth()

    shows = methods.getAllAlphabetical(client) 
    df = pd.DataFrame(shows)
    #df.to_csv("shows.csv", index=True)
    with open("shows.json", "w") as f:
        f.write(json.dumps(shows))
    print(len(shows))

    categories = methods.getCategories(client)
    df = pd.DataFrame(categories)
    #df.to_csv("categories.csv", index=True)
    with open("categories.json", "w") as f:
        f.write(json.dumps(categories))
    print(len(categories))

    season_tags = methods.getSeasonTags(client)
    df = pd.DataFrame(season_tags)
    #df.to_csv("season_tags.csv", index=True)
    with open("season_Tags.json", "w") as f:
        f.write(json.dumps(season_tags))
    print(len(season_tags))

if __name__ in '__main__':
    main()