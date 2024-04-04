import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
hobbies = ["Volleyball", "Drawing", "Dance", "Music", "Theatre", "Culinary", "Gardening", "Woodworking", "Sculpture", "Reading", "Ice Skating", "Roller Skating", "Bowling", "Badminton", "Yoga", "Pilates", "Boxing", "Muay Thai", "Cycling", "Judo", "Brazilian Jiu Jitsu", "Meditation", "Running", "Taekwondo", "Karate", "Chess", "Board Games", "Soccer", "Football", "Painting"]

for hobby in hobbies:
    print(f"Searching for {hobby} locations in Toronto...")

    # Files for writing the names and SQL insert statements for each hobby
    names_file_path = f'{hobby.lower()}_places_names.txt'
    sql_file_path = f'{hobby.lower()}_places_insert.sql'

    with open(names_file_path, 'w') as names_file, open(sql_file_path, 'w') as sql_file:
        # Text Search request to find places related to the hobby
        text_search_url = 'https://places.googleapis.com/v1/places:searchText'
        text_search_headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'places.name,places.id,places.displayName,places.formattedAddress,places.location'
        }
        queries = [{'textQuery': f"{hobby} in Toronto"},  {'textQuery': f"{hobby} classes in Toronto"}]
        unique_place_ids = set()

        # Aggregate all unique place IDs from both queries
        for query in queries:
            response = requests.post(text_search_url, headers=text_search_headers, json=query)
            text_search_results = response.json()

            for place in text_search_results['places']: 
                place_id = place.get('id')  # Adjust 'id' if your API uses 'place_id' or another key
                if place_id:
                    unique_place_ids.add(place_id)

        # Iterate through the Text Search results to get place details
        for place_id in unique_place_ids:
            place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json'
            place_details_params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,geometry,website,url',
                'key': api_key
            }

            # Send the Place Details request
            place_details_response = requests.get(place_details_url, params=place_details_params)
            place_details = place_details_response.json().get('result', {})

            # Extract required details
            name = place_details.get('name')
            address = place_details.get('formatted_address')
            geometry = place_details.get('geometry', {})
            location = geometry.get('location', {})
            latitude = location.get('lat')
            longitude = location.get('lng')
            website = place_details.get('website') or place_details.get('url')  # Use 'url' as fallback

            # Write the place name to the file
            names_file.write(f"{name}\n")

            name_escaped = name.replace("'", "''")
            address_escaped = address.replace("'", "''")
            website_escaped = website.replace("'", "''")

            # Write the SQL insert statement to the file
            sql_file.write(
                f"INSERT INTO locations (name, address, latitude, longitude, cost, popularity, booking_url, created_at) "
                f"VALUES ('{name_escaped}', '{address_escaped}', {latitude}, {longitude}, '$', null, '{website_escaped}', NOW());\n"
            )

            # Print the details for confirmation
            print(f"Name: {name}")
            print(f"Address: {address}")
            print(f"Latitude: {latitude if latitude else 'No latitude available'}")
            print(f"Longitude: {longitude if longitude else 'No longitude available'}")
            print(f"Website: {website if website else 'No website available'}")
            print("-" * 30)