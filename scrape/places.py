import googlemaps
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Your list of hobbies
# hobbies = ["Hockey", "Baseball", "Swimming", "Rugby", "Frisbee", "Lacrosse", "Volleyball", "Drawing", "Dance", "Music", "Theatre", "Culinary", "Gardening", "Woodworking", "Sculpture", "Reading", "Ice Skating", "Roller Skating", "Bowling", "Badminton", "Yoga", "Pilates", "Boxing", "Muay Thai", "Cycling", "Judo", "Brazilian Jiu Jitsu", "Meditation", "Running", "Taekwondo", "Karate", "Chess", "Board Games", "Soccer", "Football", "Painting"]
hobbies = ["Hockey"]
# Create a client
gmaps = googlemaps.Client(key=api_key)

# # Files to write the SQL queries and location names
# sql_file = open('locations.sql', 'w')
# names_file = open('location_names.txt', 'w')

for hobby in hobbies:
    query = f"{hobby} in Toronto"
    results = gmaps.places(query)
    print(results)
    # for result in results['results']:
        # name = result['name']
        # address = result.get('formatted_address', 'Unknown address').replace('\n', ' ').replace("'", "''")
        # location = result['geometry']['location']
        # latitude = location['lat']
        # longitude = location['lng']
        # print(result)
        # Get the website or Google Maps link
        # website = result.get('website')
        # if not website:
        #     # Get the place details to get the Google Maps URL
        #     place_id = result['place_id']
        #     place_details = gmaps.place(place_id)
        #     website = place_details['result'].get('url')

        # Write the SQL query to the file
        # sql_query = f"""INSERT INTO locations (name, address, latitude, longitude, cost, popularity, booking_url, created_at) VALUES ('{name.replace("'", "''")}', '{address}', {latitude}, {longitude}, '$', null, '{website}', NOW());\n"""
        # sql_file.write(sql_query)

        # # Write the location name to the file
        # names_file.write(f"{name}\n")


# # Close the files
# sql_file.close()
# names_file.close()