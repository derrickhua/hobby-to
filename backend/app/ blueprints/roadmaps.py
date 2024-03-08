from flask import Blueprint, request, jsonify, current_app
from redis import Redis
from marshmallow import ValidationError
from app import db  
import json
from sqlalchemy.exc import SQLAlchemyError  # Import this for handling database errors
from sqlalchemy import func
from schemas import RoadmapSchema, RoadmapNodeSchema
from models import Roadmap, RoadmapNode, Hobby

# Define Variables
roadmaps_bp = Blueprint('roadmaps_bp', __name__)
roadmap_schema = RoadmapSchema()
roadmaps_schema = RoadmapSchema(many=True)
roadmap_node_schema = RoadmapNodeSchema(many=True)
redis_client = Redis.from_url(current_app.config['REDIS_URL'])

@roadmaps_bp.route('/api/roadmaps', methods=['POST'])
def create_roadmap():
    json_data = request.get_json()
    if not json_data:
        current_app.logger.warning('Attempt to create roadmap with no input data')
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = roadmap_schema.load(json_data)
    except ValidationError as err:
        current_app.logger.warning(f'Validation error on roadmap creation: {err.messages}')
        return jsonify(err.messages), 422

    try:
        roadmap = Roadmap(
            title=data['title'],
            description=data.get('description'),
            hobby_id=data['hobby_id'],
            user_id=data.get('user_id')
        )
        db.session.add(roadmap)
        db.session.commit()
        
        current_app.logger.info(f'Roadmap created successfully: {roadmap.roadmap_id}')
        return jsonify({'message': 'Roadmap created', 'roadmap_id': roadmap.roadmap_id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating roadmap: {e}')
        return jsonify({'message': 'Failed to create roadmap'}), 500
    
@roadmaps_bp.route('/api/roadmaps', methods=['GET'])
def get_roadmaps():
    search_query = request.args.get('search', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Adjust based on your needs
    
    # Construct a cache key that reflects the current state of query parameters
    cache_key = f"roadmaps:{search_query or 'all'}:{category or 'all'}:{page}"

    cached_roadmaps = redis_client.get(cache_key)
    if cached_roadmaps:
        current_app.logger.info(f"Returning cached roadmaps for page {page}, search '{search_query}', category '{category}'")
        return jsonify(json.loads(cached_roadmaps)), 200

    query_obj = Roadmap.query
    if search_query:
        query_obj = query_obj.join(Hobby, Roadmap.hobby_id == Hobby.hobby_id).filter(Hobby.name.ilike(f'%{search_query}%'))
    if category in ["Arts", "Sports", "Other"]:
        query_obj = query_obj.join(Hobby, Roadmap.hobby_id == Hobby.hobby_id).filter(Hobby.category == category)

    # Apply random ordering
    query_obj = query_obj.order_by(func.random())

    pagination = query_obj.paginate(page=page, per_page=per_page, error_out=False)
    roadmaps = pagination.items
    
    serialized_roadmaps = roadmaps_schema.dump(roadmaps)
    redis_client.setex(cache_key, 3600, json.dumps(serialized_roadmaps))
    current_app.logger.info(f"Cached roadmaps for page {page}, search '{search_query}', category '{category}'")
    
    next_url = f'/api/roadmaps?page={page + 1}' if pagination.has_next else None
    prev_url = f'/api/roadmaps?page={page - 1}' if pagination.has_prev else None
    
    response = {
        'roadmaps': serialized_roadmaps,
        'next_url': next_url,
        'prev_url': prev_url,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }

    return jsonify(response), 200



@roadmaps_bp.route('/api/roadmaps/<int:roadmap_id>', methods=['GET'])
def get_roadmap_detail(roadmap_id):
    cache_key = f"roadmap_detail:{roadmap_id}"

    cached_detail = redis_client.get(cache_key)
    if cached_detail:
        current_app.logger.info(f"Returning cached detail for roadmap {roadmap_id}")
        return jsonify(json.loads(cached_detail)), 200  # Return cached data

    roadmap = Roadmap.query.get(roadmap_id)
    if not roadmap:
        current_app.logger.warning(f"Roadmap {roadmap_id} not found")
        return jsonify({'message': 'Roadmap not found'}), 404

    roadmap_detail = roadmap_schema.dump(roadmap)
    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).order_by(RoadmapNode.order).all()
    roadmap_detail['nodes'] = roadmap_node_schema.dump(nodes)

    redis_client.setex(cache_key, 3600, json.dumps(roadmap_detail)) 
    current_app.logger.info(f"Cached detail view for roadmap {roadmap_id}")
    
    return jsonify(roadmap_detail), 200