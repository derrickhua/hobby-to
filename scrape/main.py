import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import re
# Base URL of the website to resolve relative links
base_url = 'https://www.toronto.ca'

# The initial page URL that lists the community centres
initial_url = 'https://www.toronto.ca/data/parks/prd/sports/dropin/basketball/index.html'

# Table Tennis from Toronto.ca
# def scrape_initial_page(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # This will hold the URLs to scrape in the next step
#     centre_urls = []

#     listings = soup.find_all('div', class_='pfrListing')
#     for listing in listings:
#         if "Table Tennis" in listing.text:
#             h2_tag = listing.find('h2')
#             if h2_tag:
#                 a_tag = h2_tag.find('a', href=True)
#                 if a_tag:
#                     # Resolve the relative URL to an absolute URL
#                     absolute_url = urljoin(base_url, a_tag['href'])
#                     centre_urls.append(absolute_url)
    
#     return centre_urls
#  Basketball
def scrape_initial_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # This will hold the URLs and names of centers with adult basketball programs
    centre_details = []

    listings = soup.find_all('div', class_='pfrListing')
    for listing in listings:
        program_rows = listing.find_all('tr', attrs={'data-courseid': True})
        for row in program_rows:
            program_div = row.find('div', class_='coursenamemobiletable')
            if program_div and 'Basketball' in program_div.text:
                age_text = program_div.text
                # Check if the program is for adults (18 years and up)
                if any(age_indicator in age_text for age_indicator in ('17 yrs +', '18 yrs +', '19 yrs +')):
                    h2_tag = listing.find('h2')
                    if h2_tag:
                        a_tag = h2_tag.find('a', href=True)
                        if a_tag:
                            # Resolve the relative URL to an absolute URL
                            absolute_url = urljoin(base_url, a_tag['href'])
                            centre_name = a_tag.text.strip()
                            # Store details if not already included
                            if not any(centre['name'] == centre_name for centre in centre_details):
                                centre_details.append({
                                    'name': centre_name,
                                    'url': absolute_url
                                })
                    break  # Move to the next listing after finding an adult basketball program
    
    return centre_details

centre_urls = scrape_initial_page(initial_url)

def extract_lat_lng_from_anchor(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Target the specific div and then find an <a> tag within it
    target_div = soup.find('div', class_='col-md-12 col-lg-11')
    if not target_div:
        return None, None  # Or return a default value or placeholder if preferred

    a_tag = target_div.find('a', href=True)
    if not a_tag or 'location=' not in a_tag['href']:
        return None, None  # Or return a default value or placeholder if preferred
    
    # Extract the URL fragment (after '#') and decode any percent-encoded characters
    fragment = unquote(urlparse(a_tag['href']).fragment)
    params = dict(item.split("=") for item in fragment.split("&") if "=" in item)

    lat = params.get('lat')
    lng = params.get('lng')

    return lat, lng

def scrape_centre_details(centre_urls):
    details = []
    for centre in centre_urls:  # Assuming centre_urls is a list of dictionaries
        url = centre['url']  # Correctly extract the URL from each dictionary
        response = requests.get(url)  # This now correctly passes a URL string to requests.get()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the name of the community centre
        centre_name_h1 = soup.select_one('.col-md-12.col-lg-11 h1')
        centre_name = centre_name_h1.text.strip() if centre_name_h1 else 'Centre Name not found'

        # Extract the address
        address_span = soup.select_one('.col-md-12.col-lg-11 span')
        address = address_span.text.strip() if address_span else 'Address not found'

        # Attempt to extract latitude and longitude
        map_link = soup.select_one('.col-md-12.col-lg-11 a[href*="lat="]')
        lat, lng = 'Latitude not found', 'Longitude not found'
        if map_link:
            href = map_link.get('href', '')
            lat_lng_match = re.search(r'lat=([-\d.]+)&lng=([-\d.]+)', href)
            if lat_lng_match:
                lat, lng = lat_lng_match.groups()

        details.append({
            'name': centre_name,
            'address': address,
            'latitude': lat,
            'longitude': lng,
            'url': url  # Include the URL in the details
        })
    
    return details

existing_centre_names = """
Antibes Community Centre
Birchmount Community Centre
Birkdale Community Centre
Cummer Park Community Centre
Dennis R. Timbrell Resource Centre
Don Montgomery Community Centre
Driftwood Community Recreation Centre
Earl Bales Community Centre
Edithvale Community Centre
Ellesmere Community Centre
Ethennonnhawahstihnen' Community Recreation Centre and Library
Fairfield Seniors' Centre
Falstaff Community Centre
Frankland Community Centre
Goulding Community Centre
Heron Park Community Centre
Jenner Jean-Marie Community Centre
Jimmie Simpson Recreation Centre
L'Amoreaux Community Recreation Centre
Lawrence Heights Community Centre
Main Square Community Centre
Matty Eckler Recreation Centre
Mitchell Field Community Centre
Northwood Community Centre
One Yonge Community Recreation Centre
Parkway Forest Community Centre
Regent Park Community Centre
Scarborough Village Recreation Centre
Thistletown Seniors' Centre
Trinity Community Recreation Centre
Warden Hilltop Community Centre
Wellesley Community Centre
West Acres Seniors Centre
York Recreation Centre
Athletic Centre
""".split('\n')

def generate_sql_queries_and_filter_names(centre_details, existing_centre_names):
    sql_queries = []
    unique_centre_names = []  # To track new, non-duplicate centers
    duplicate_centre_names = []  # To track duplicates

    for detail in centre_details:
        # Extract and format details
        name = detail['name'].replace("'", "''")
        address = detail.get('address', 'Unknown Address').replace("'", "''")
        latitude = detail.get('latitude', 'NULL')
        longitude = detail.get('longitude', 'NULL')
        booking_url = detail.get('url', '').replace("'", "''")

        # Check if the centre name is not in the provided list of existing names
        if detail['name'] not in existing_centre_names:
            if detail['name'] not in unique_centre_names:
                unique_centre_names.append(detail['name'])  # Add to our unique list
                # Construct the SQL query
                query = f"INSERT INTO locations (name, address, latitude, longitude, cost, popularity, booking_url, created_at) VALUES ('{name}', '{address}', {latitude}, {longitude}, '$', null, '{booking_url}', NOW());"
                sql_queries.append(query)
            else:
                # If already in unique_centre_names, it's a duplicate within the new data
                duplicate_centre_names.append(detail['name'])
        else:
            # If in existing_centre_names, it's a duplicate with the pre-existing data
            duplicate_centre_names.append(detail['name'])

    # Save SQL queries to a file, now excluding duplicates
    with open('insert_queries_filtered.sql', 'w') as file:
        for query in sql_queries:
            file.write(query + "\n")

    # Save filtered centre names to a separate file
    with open('filtered_centre_names.txt', 'w') as file:
        for name in unique_centre_names:
            file.write(name + "\n")

    # Save duplicates to a third file
    with open('duplicates.txt', 'w') as file:
        for name in duplicate_centre_names:
            file.write(name + "\n")

    return sql_queries, unique_centre_names, duplicate_centre_names

details = scrape_centre_details(centre_urls)
sql_queries, unique_centre_names, duplicate_centre_names = generate_sql_queries_and_filter_names(details, existing_centre_names)
