from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from redis import Redis
from ..database import db
from sqlalchemy import text
import json
from ..models import Hobby, Location, HobbyLocation  # Import HobbyLocation if it's a new model
from ..schemas import HobbySchema, LocationSchema
from ..redis_client import redis_client
import decimal
# Define Variables
hobby_bp = Blueprint('hobby_bp', __name__)  
hobby_schema = HobbySchema()
hobbies_schema = HobbySchema(many=True)  
location_schema = LocationSchema(many=True)

@hobby_bp.route('/search', methods=['GET'])
def search_hobbies():
    query_param = request.args.get('query', '')
    cost = request.args.getlist('cost')  # This will be a list like ['$','$$','$$$']
    category = request.args.get('category', None)
    cache_key = f"search:{query_param}:{category}:{':'.join(cost)}"

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            current_app.logger.info(f"Returning cached results for {cache_key}")
            return jsonify(json.loads(cached_data.decode('utf-8'))), 200

        # Start with the basic part of the query
        sql_query = """
            SELECT l.location_id, l.name, l.address, l.latitude, l.longitude, l.cost, l.popularity, l.booking_url FROM hobbies h
            JOIN hobby_location hl ON h.hobby_id = hl.hobby_id
            JOIN locations l ON hl.location_id = l.location_id
            WHERE (h.name ILIKE :query_param OR h.sub_category ILIKE :query_param OR :query_param IS NULL)
            AND (h.category = :category OR :category IS NULL)
        """

        # Dynamically build the cost condition if there are cost filters
        if cost:
            cost_conditions = " OR ".join([f"l.cost = '{c}'" for c in cost])
            sql_query += f" AND ({cost_conditions})"

        sql_query += " ORDER BY GREATEST(similarity(h.name, :query_param), similarity(h.sub_category, :query_param)) DESC;"

        params = {'query_param': f'%{query_param}%', 'category': category}

        # Execute the query
        with db.engine.connect() as connection:
            result = connection.execute(text(sql_query), params)

            # Define the column names
            column_names = ['location_id', 'name', 'address', 'latitude', 'longitude', 'cost', 'popularity', 'booking_url']

            # Convert the row into a dictionary
            search_results = [dict(zip(column_names, row)) for row in result]

            # Convert datetime objects into strings and Decimal objects into floats
            for result in search_results:
                for key, value in result.items():
                    if isinstance(value, decimal.Decimal):
                        result[key] = float(value)

        redis_client.setex(cache_key, 3600, json.dumps(search_results).encode('utf-8'))
        current_app.logger.info(f"Cached search results for {cache_key}")
        return jsonify(search_results), 200
    except Exception as e:
        current_app.logger.error(f'Error during search: {e}')
        return jsonify({"message": "An error occurred while searching for hobbies", "error": str(e)}), 500


@hobby_bp.route('/category', methods=['GET'])
def get_hobbies_by_category():
    category = request.args.get('category')
    cache_key = f"hobbies_by_category:{category}"
    try:
        if category and category in ["Arts", "Sports", "Other"]:
            cached_hobbies = redis_client.get(cache_key)
            if cached_hobbies:
                return jsonify(json.loads(cached_hobbies)), 200

            hobbies = Hobby.query.filter_by(category=category).all()
            serialized_hobbies = hobbies_schema.dump(hobbies)
            redis_client.setex(cache_key, 3600, json.dumps(serialized_hobbies))  # Cache for 1 hour
            return jsonify(serialized_hobbies), 200
        else:
            return jsonify({"message": "Invalid or missing category"}), 400
    except Exception as e:
        current_app.logger.error(f'Error fetching hobbies for category "{category}": {e}')
        return jsonify({"message": "An error occurred"}), 500

@hobby_bp.route('/<int:hobby_id>', methods=['GET'])
def get_hobby(hobby_id):
    try:
        hobby = Hobby.query.get(hobby_id)
        if hobby is None:
            current_app.logger.warning(f'Hobby with ID {hobby_id} not found.')
            return jsonify({"message": "Hobby not found"}), 404

        current_app.logger.info(f"Retrieved hobby with ID {hobby_id}.")
        return jsonify(hobby_schema.dump(hobby)), 200
    except Exception as e:
        current_app.logger.error(f'Error retrieving hobby with ID {hobby_id}: {e}')
        return jsonify({"message": "An error occurred while fetching the hobby", "error": str(e)}), 500

@hobby_bp.route('/<int:hobby_id>/locations', methods=['GET'])
def get_hobby_locations(hobby_id):
    cache_key = f"hobby_locations:{hobby_id}"
    try:
        cached_locations = redis_client.get(cache_key)
        if cached_locations:
            return jsonify(json.loads(cached_locations.decode('utf-8'))), 200

        # Query the HobbyLocation table to find related locations for the given hobby_id
        hobby_location_links = HobbyLocation.query.filter_by(hobby_id=hobby_id).all()
        if not hobby_location_links:
            return jsonify({"message": "No locations found for the specified hobby"}), 404
        
        location_ids = [link.location_id for link in hobby_location_links]
        
        locations = Location.query.filter(Location.location_id.in_(location_ids)).all()

        serialized_locations = location_schema.dump(locations, many=True)
        redis_client.setex(cache_key, 3600, json.dumps(serialized_locations).encode('utf-8'))  # Cache for 1 hour
        return jsonify(serialized_locations), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching locations for hobby_id {hobby_id}: {e}')
        return jsonify({"message": "An error occurred"}), 500
