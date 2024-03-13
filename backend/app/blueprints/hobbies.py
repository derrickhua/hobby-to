from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from redis import Redis
from ..database import db
from sqlalchemy import text
import json
from ..models import Hobby, Location, HobbyLocation  # Import HobbyLocation if it's a new model
from ..schemas import HobbySchema, LocationSchema
from ..redis_client import redis_client

# Define Variables
hobby_bp = Blueprint('hobby_bp', __name__)  
hobby_schema = HobbySchema()
hobbies_schema = HobbySchema(many=True)  
location_schema = LocationSchema(many=True)

@hobby_bp.route('/search', methods=['GET'])
def search_hobbies():
    query = request.args.get('query', '')
    cost = request.args.getlist('cost')
    category = request.args.get('category', None)
    cache_key = f"search:{query}:{category}:{':'.join(cost)}"

    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            current_app.logger.info(f"Returning cached results for {cache_key}")
            return jsonify(json.loads(cached_data)), 200

        # Modify this query to include joins with the HobbyLocation table
        sql_query = text("""
            SELECT h.*, l.* FROM hobbies h
            JOIN hobby_location hl ON h.hobby_id = hl.hobby_id
            JOIN locations l ON hl.location_id = l.location_id
            WHERE (:query IS NULL OR h.name ILIKE :query OR h.sub_category ILIKE :query)
            AND (:category IS NULL OR h.category = :category)
            AND (ARRAY[:cost]::text[] IS NULL OR l.cost = ANY(ARRAY[:cost]::text[]))
            ORDER BY GREATEST(similarity(h.name, :query), similarity(h.sub_category, :query)) DESC;
        """)

        result = db.engine.execute(sql_query, query='%'+query+'%', cost=cost, category=category)
        # search_results = process_search_results(result)

        # redis_client.setex(cache_key, 3600, json.dumps(search_results))
        # current_app.logger.info(f"Cached search results for {cache_key}")
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f'Error during search: {e}')
        return jsonify({"message": "An error occurred while searching for hobbies", "error": str(e)}), 500

def process_search_results(result):
    # Implement the logic to process and convert SQL results into a structured JSON format.
    # This placeholder function needs to be replaced with actual logic.
    return [{"placeholder": "Implement logic to structure SQL results into JSON"}]

@hobby_bp.route('', methods=['GET'])
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
    
@hobby_bp.route('/categories', methods=['GET'])
def get_hobby_categories():
    try:
        categories = ["Arts", "Sports", "Other"]
        return jsonify(categories), 200
    except Exception as e:
        current_app.logger.error(f'Failed to fetch hobby categories: {e}')
        return jsonify({"message": "An error occurred while fetching the hobby categories"}), 500

@hobby_bp.route('/categories/<category>/hobbies', methods=['GET'])
def get_hobbies_by_general_category(category):
    cache_key = f"general_category_hobbies:{category}"
    try:
        if category in ["Arts", "Sports", "Other"]:
            cached_hobbies = redis_client.get(cache_key)
            if cached_hobbies:
                return jsonify(json.loads(cached_hobbies)), 200

            hobbies = Hobby.query.filter_by(category=category).all()
            serialized_hobbies = hobbies_schema.dump(hobbies)
            redis_client.setex(cache_key, 3600, json.dumps(serialized_hobbies))  # Cache for 1 hour
            return jsonify(serialized_hobbies), 200
        else:
            return jsonify({"message": "Invalid category"}), 400
    except Exception as e:
        current_app.logger.error(f'Error fetching hobbies for general category "{category}": {e}')
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
            return jsonify(json.loads(cached_locations)), 200

        locations = Location.query.filter_by(hobby_id=hobby_id).all()
        if not locations:
            return jsonify({"message": "No locations found for the specified hobby"}), 404
        
        serialized_locations = location_schema.dump(locations)
        redis_client.setex(cache_key, 3600, json.dumps(serialized_locations))  # Cache for 1 hour
        return jsonify(serialized_locations), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching locations for hobby_id {hobby_id}: {e}')
        return jsonify({"message": "An error occurred"}), 500