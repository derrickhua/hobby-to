from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.models import Hobby, Location  
from app.schemas import HobbySchema, LocationSchema

# Create a Blueprint for this module
hobby_bp = Blueprint('hobby_bp', __name__)  # Change 'model_bp' to a name relevant to your model
hobby_schema = HobbySchema()
hobbies_schema = HobbySchema(many=True)  
location_schema = LocationSchema(many=True)

# GET /api/hobbies/search?query={query}
# GET /api/hobbies/categories
# GET /api/hobbies?category={category}
# GET /api/categories
# GET /api/categories/{category_id}/hobbies
# GET /api/hobbies/{hobby_id}
# GET /api/hobbies/{hobby_id}/locations

@hobby_bp.route('/search', methods=['GET'])
def search_hobbies():
    query = request.args.get('query')
    if not query:
        current_app.logger.warning('No query provided for hobby search.')
        return jsonify({"message": "No query provided"}), 400

    try:
        hobbies = Hobby.query.filter(Hobby.name.ilike(f'%{query}%')).all()
        current_app.logger.info(f"Hobbies search completed with query '{query}'.")
        return jsonify(hobbies_schema.dump(hobbies)), 200
    except Exception as e:
        current_app.logger.error(f'Error searching hobbies with query {query}: {e}')
        return jsonify({"message": "An error occurred while searching for hobbies", "error": str(e)}), 500

@hobby_bp.route('', methods=['GET'])
def get_hobbies_by_category():
    category = request.args.get('category')
    try:
        if category and category in ["Arts", "Sports", "Other"]:
            hobbies = Hobby.query.filter_by(category=category).all()
            return jsonify(hobbies_schema.dump(hobbies)), 200
        else:
            return jsonify({"message": "Invalid or missing category"}), 400
    except Exception as e:
        current_app.logger.error(f'Failed to fetch hobbies for category "{category}": {e}')
        return jsonify({"message": "An error occurred while fetching hobbies"}), 500

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
    try:
        if category in ["Arts", "Sports", "Other"]:
            hobbies = Hobby.query.filter_by(category=category).all()
            return jsonify(hobbies_schema.dump(hobbies)), 200
        else:
            return jsonify({"message": "Invalid category"}), 400
    except Exception as e:
        current_app.logger.error(f'Failed to fetch hobbies for category "{category}": {e}')
        return jsonify({"message": "An error occurred while fetching hobbies for the category"}), 500

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
    try:
        locations = Location.query.filter_by(hobby_id=hobby_id).all()
        if not locations:
            current_app.logger.info(f'No locations found for hobby_id: {hobby_id}')
            return jsonify({"message": "No locations found for the specified hobby"}), 404
        return jsonify(location_schema.dump(locations)), 200
    except ValidationError as err:
        current_app.logger.warning(f'Validation error while fetching locations for hobby_id {hobby_id}: {err.messages}')
        return jsonify({"message": "Validation error", "errors": err.messages}), 422
    except Exception as e:
        current_app.logger.error(f'Unexpected error while fetching locations for hobby_id {hobby_id}: {e}')
        return jsonify({"message": "An error occurred while fetching locations", "error": str(e)}), 500
