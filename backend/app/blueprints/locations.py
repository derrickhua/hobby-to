from flask import Blueprint, jsonify, current_app
from redis import Redis
import json
from ..models import Location
from ..schemas import LocationSchema
from ..redis_client import redis_client
# Define Variables
location_bp = Blueprint('location_bp', __name__)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

@location_bp.route('/api/locations', methods=['GET'])
def get_locations():
    cache_key = 'all_locations'
    try:
        cached_locations = redis_client.get(cache_key)
        if cached_locations:
            # Cache hit, return the cached data
            return jsonify(json.loads(cached_locations)), 200
        
        locations = Location.query.all()
        serialized_locations = locations_schema.dump(locations)
        redis_client.setex(cache_key, 3600, json.dumps(serialized_locations))  
        return jsonify(serialized_locations), 200
    except Exception as e:
        current_app.logger.error(f'Unexpected error while fetching all locations: {e}')
        return jsonify({"message": "An error occurred while fetching locations", "error": str(e)}), 500

@location_bp.route('/api/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    cache_key = f'location:{location_id}'
    try:
        cached_location = redis_client.get(cache_key)
        if cached_location:
            return jsonify(json.loads(cached_location)), 200

        location = Location.query.get(location_id)
        if location is None:
            return jsonify({"message": "Location not found"}), 404
        
        serialized_location = location_schema.dump(location)
        redis_client.setex(cache_key, 3600, json.dumps(serialized_location))  
        return jsonify(serialized_location), 200
    except Exception as e:
        current_app.logger.error(f'Unexpected error while fetching location with ID {location_id}: {e}')
        return jsonify({"message": "An error occurred while fetching the location", "error": str(e)}), 500
